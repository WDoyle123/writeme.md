from flask import request, Flask, Response
from flask_cors import CORS
import requests
import logging

server = Flask(__name__)
CORS(server)

logging.basicConfig(level=logging.DEBUG)

@server.route('/', defaults={'path': ''})
@server.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Determine target URL based on the path
    if path.startswith("api/upload"):
        target_url = f"http://upload-download-service:8080/{path[len('api/'):]}"
    else:
        target_url = f"http://readme-website-service:4173/{path}"

    query_params = request.args
    headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'content-length']}

    server.logger.debug(f"Requesting URL: {target_url} with params: {query_params} and headers: {headers}")

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=query_params,
            data=request.get_data(),
            allow_redirects=False,
            stream=True
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

        server.logger.debug("Successfully retrieved response from target service")
        return Response(resp.iter_content(chunk_size=1024), resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        server.logger.error(f"Request failed: {str(e)}")
        return Response(f"An error occurred while trying to proxy request: {str(e)}", status=502)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)

