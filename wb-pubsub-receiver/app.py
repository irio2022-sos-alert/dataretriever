import os

import ping_pb2
import ping_pb2_grpc
import grpc
from flask import Flask, request

app = Flask(__name__)


@app.before_first_request
def init():
    global alertmanager_endpoint
    alertmanager_endpoint = os.getenv("WB_RECEIVER_ENDPOINT", "[::]:50053")


@app.route("/", methods=['GET'])
def test():
    return "test"

@app.route("/transform", methods=['POST'])
def transform():
    return f"test {request.json}"


if __name__ == "__main__":
    app.run()