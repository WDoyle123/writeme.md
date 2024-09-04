import json
import logging
import os
import sys
import time

import pika
from send.email import notification


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("Waiting...")

    try:
        logger.info("Ready...")
        rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = connection.channel()

        readme_queue_name = os.environ.get("README_QUEUE", "readme")

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                logger.info(f"Received data: {data}")
                correlation_id = properties.correlation_id
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                return

            try:
                print(data['repo_name'])
                notification(data)
            except Exception as e:
                logger.error(f"Error: {e}")

        channel.basic_consume(
            queue=readme_queue_name, on_message_callback=callback, auto_ack=True
        )

        logger.info(
            f"Waiting for messages in queue: {readme_queue_name}. To exit press CTRL+C"
        )
        channel.start_consuming()

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        if "connection" in locals() and connection.is_open:
            connection.close()
            logger.info("Connection closed")

if __name__ == "__main__":
    main()
