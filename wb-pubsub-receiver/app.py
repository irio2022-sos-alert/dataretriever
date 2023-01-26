import os
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
from flask import Flask, request

app = Flask(__name__)


@app.before_first_request
def init():
    global project_id, topic_id
    project_id = "cloud-run-grpc-ping"
    topic_id = "whistleblower-topic"

@app.route("/", methods=['GET'])
def test():
    return "test"

@app.route("/transform", methods=['POST'])
def transform():
    logging.info("Received post")
    logging.info(f"json: {request.json}")
    return "OK"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()