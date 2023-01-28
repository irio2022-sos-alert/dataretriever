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
    global whistleblower_endpoint, dataretriever_endpoint
    whistleblower_endpoint = os.getenv("WB_ENDPOINT")
    dataretriever_endpoint = os.getenv("DR_ENDPOINT")


@app.route("/", methods=['GET'])
def default():
    return "OK"


@app.route("/transform-wb", methods=['POST'])
def transform_wb():
    dict = create_dict_from_req(request)
    send_wb_message(dict)
    return "OK"

@app.route("/transform-dr", methods=['POST'])
def transform_dr():
    dict = create_dict_from_req(request)
    send_dr_message(dict)
    return "OK"


def create_dict_from_req(request):
    dict = ast.literal_eval(request.data.decode('utf-8'))
    dict = dict['message']['data']
    dict = ast.literal_eval(base64.b64decode(dict).decode('utf-8'))
    return dict

def create_wb_message(dict):
    logging.info(f"id: {dict['service_id']}, ts: {dict['timestamp']}, okay: {dict['okay']}")
    return ping_pb2.PingStatus(service_id=dict['service_id'], timestamp=dict['timestamp'], okay=(dict['okay']==1))


def create_dr_message(dict):
    return ping_pb2.PingRequest(service_id=dict['service_id'], domain=dict['domain'])


def send_wb_message(dict):
    mess = create_wb_message(dict)
    logging.info(f"whistleblower_endpoint: {whistleblower_endpoint}")
    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        ping_result = stub.AckPingStatus(mess)


def send_dr_message(dict):
    mess = create_dr_message(dict)
    with grpc.secure_channel(dataretriever_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.DataRetrieverStub(channel)
        ping_result = stub.PingDomain(mess)


if __name__ == "__main__":
    app.run()