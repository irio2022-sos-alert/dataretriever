import os
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
from flask import Flask, request
import ast
import base64

app = Flask(__name__)


@app.before_first_request
def init():
    global project_id, topic_id, whistleblower_endpoint
    project_id = "cloud-run-grpc-ping"
    topic_id = "whistleblower-topic"
    whistleblower_endpoint = "whistleblower-app-6oed3mtq4a-lz.a.run.app"


@app.route("/", methods=['GET'])
def test():
    return "OK"


@app.route("/transform", methods=['POST'])
def transform():
    send_to_whistleblower(request)
    return "OK"


def create_whistleblower_message(request):
    dict = ast.literal_eval(request.data.decode('utf-8'))
    req = dict['message']['data']
    req = ast.literal_eval(base64.b64decode(req).decode('utf-8'))
    return ping_pb2.CalculateSum(domain=req['domain'], time=req['time'])


def send_to_whistleblower(request):
    mess = create_whistleblower_message(request)
    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        ping_result = stub.SumResponseTimes(mess)


if __name__ == "__main__":
    app.run()