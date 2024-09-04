import json
import logging
import os
import time
import tiktoken 

import pika
from agent_functions.reader import download_repo, read_code
from agent_functions.writer import write_readme 

from agent_functions.agents import llm_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_connection():
    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        heartbeat=60,  
        blocked_connection_timeout=300  
    )
    return pika.BlockingConnection(parameters)

def publish_with_retry(channel, result_queue_name, result, correlation_id, max_retries=5):
    for attempt in range(max_retries):
        try:
            if channel.is_closed:
                connection = create_connection()
                channel = connection.channel()
            
            channel.basic_publish(
                exchange="",
                routing_key=result_queue_name,
                body=json.dumps(result),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    correlation_id=correlation_id,
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                ),
            )
            logger.info(f"Result sent to {result_queue_name} queue")
            return
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection error on publish attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(5)
        except Exception as err:
            logger.error(f"Failed to publish message: {err}")
    logger.error("Max retries reached. Failed to publish message.")

def main():
    while True:
        try:
            connection = create_connection()
            channel = connection.channel()
            queue_name = os.environ.get("REPO_QUEUE", "repo")
            result_queue_name = os.environ.get("README_QUEUE", "readme")

            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_declare(queue=result_queue_name, durable=True)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body)
                    logger.info(f"Received data: {data}")
                    repo_name = data["repo_name"]
                    email = data["email"]
                    openai_api_key = data["openai_api_key"]
                    openai_model = data["openai_model"]
                    logger.info(f"LLM_CONFIG:{llm_config(openai_api_key, openai_model)}")
                    correlation_id = properties.correlation_id

                    runtime(repo_name, email, openai_api_key, openai_model, ch, result_queue_name, correlation_id)

                except Exception as e:
                    logger.error(f"Error processing message: {e}")

                finally:
                    logger.info("Finished processing message, waiting for the next one.")

            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            logger.info(f"Waiting for messages in queue: {queue_name}. To exit press CTRL+C")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            try:
                if 'connection' in locals() and connection.is_open:
                    connection.close()
                    logger.info("Connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")

# Function to count tokens in text using tiktoken
def count_tokens(text, model="gpt-3.5-turbo"):
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = tokenizer.encode(text)
    return len(tokens)

def runtime(repo_name, email, openai_api_key, openai_model, channel, result_queue_name, correlation_id):
    repo_path = download_repo(repo_name)
    read_code(repo_path, openai_api_key, openai_model)
    final_readme = write_readme("groupchat.txt", repo_name, openai_api_key, openai_model)

    result = {"email": email, "repo_name": repo_name, "readme_content": final_readme}
    logger.info(result)

    publish_with_retry(channel, result_queue_name, result, correlation_id)
    cleanup_files()

def cleanup_files():
    files_to_delete = ["groupchat.txt", "approved_notes.txt", "writer_output.txt", "readme.md"]
    
    for file_name in files_to_delete:
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
                logger.info(f"{file_name} has been deleted.")
            else:
                logger.info(f"{file_name} does not exist.")
        except Exception as e:
            logger.error(f"Error deleting {file_name}: {e}")

if __name__ == "__main__":
    main()

