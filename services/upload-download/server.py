import pika, gridfs
from flask import request, send_file, jsonify, Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import logging

from storage import util

server = Flask(__name__)
CORS(server)

mongo_repo = PyMongo(server, uri="mongodb://host.minikube.internal:27017/repos")  
mongo_readme = PyMongo(server, uri="mongodb://host.minikube.internal:27017/readme")

fs_repo = gridfs.GridFS(mongo_repo.db)
fs_readme = gridfs.GridFS(mongo_readme.db)

connection_params = pika.ConnectionParameters(
    "rabbitmq",
    heartbeat=120,        
    blocked_connection_timeout=300,  
    connection_attempts=3, 
    retry_delay=5         
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

logging.basicConfig(level=logging.DEBUG)

@server.route("/upload", methods=["POST"])
def upload():

    # check if json data is there
    if not request.is_json:
        return jsonify({"error": "invalid input, json expected"}), 400
    data = request.get_json()
    email = data.get('email')
    repository_name = data.get('repositoryName')
    openai_api_key = data.get('openaiApiKey')
    openai_model = data.get('openaiModel')

    if not email or not repository_name or not openai_api_key or not openai_model:
        return jsonify({"error": "missing data"}), 400

    try:
        util.upload_metadata(email, repository_name, openai_api_key, openai_model, fs_repo, channel)
        return jsonify({"message": "process initiated successfully"}), 200

    except Exception as e:
            print(e)
            return jsonify({"error": "internal server error"}), 500
           
@server.route("/download", methods=["get"])
def download():

        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400
        try:
            out = fs_readme.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.md')
        except Exception as err:
            print(err)
            return "internal server error", 500

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
