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
    global project_id, topic_id, whistleblower_endpoint, dataretriever_endpoint
    project_id = "cloud-run-grpc-ping"
    topic_id = "whistleblower-topic"
    whistleblower_endpoint = "whistleblower-app-6oed3mtq4a-lz.a.run.app"
    dataretriever_endpoint = "dataretriever-app-6oed3mtq4a-lz.a.run.app"


@app.route("/", methods=['GET'])
def test():
    return "OK"


@app.route("/transform-wb", methods=['POST'])
def transform():
    dict = create_dict_from_req(request)
    send_wb_message(dict)
    return "OK"

@app.route("/transform-dr", methods=['POST'])
def transform():
    dict = create_dict_from_req(request)
    send_dr_message(dict)
    return "OK"


def create_dict_from_req(request):
    dict = ast.literal_eval(request.data.decode('utf-8'))
    dict = dict['message']['data']
    dict = ast.literal_eval(base64.b64decode(dict).decode('utf-8'))
    return dict

def create_wb_message(dict):
    return ping_pb2.PingStatus(domain=dict['domain'], time=dict['time'], okay=dict['okay'])


def create_dr_message(dict):
    return ping_pb2.PingRequest(domain=dict['domain'])


def send_wb_message(dict):
    mess = create_wb_message(dict)
    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        ping_result = stub.PingStatus(mess)


def send_dr_message(dict):
    mess = create_dr_message(dict)
    with grpc.secure_channel(dataretriever_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.DataRetrieverStub(channel)
        ping_result = stub.PingRequest(mess)


if __name__ == "__main__":
    app.run()