import os
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
from flask import Flask, request

app = Flask(__name__)


@app.before_first_request
def init():
    global project_id, topic_id, whistleblower_endpoint
    project_id = "cloud-run-grpc-ping"
    topic_id = "whistleblower-topic"
    whistleblower_endpoint = ""


@app.route("/", methods=['GET'])
def test():
    return "test"


@app.route("/transform", methods=['POST'])
def transform():
    send_to_whistleblower(request)
    return "OK"


def create_whistleblower_message(request):
    return ping_pb2.CalculateSum(domain="google.com", time=22.0)


def send_to_whistleblower(request):
    mess = create_whistleblower_message(request)

    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        ping_result = stub.SumResponseTimes(mess)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()