import pika, json

def upload_metadata(email, repo_name, openai_api_key, openai_model, fs, channel):
    message = {
        "email": email,
        "repo_name": repo_name,
        "openai_api_key": openai_api_key,
        "openai_model": openai_model,

    }
    try:
        channel.basic_publish(
            exchange="",
            routing_key="repo",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        return "internal server error", 500
