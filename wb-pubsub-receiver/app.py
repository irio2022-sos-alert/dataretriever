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


@app.route("/transform-wb", methods=['POST'])
def transform_wb():
    dict = create_dict_from_req(request)
    return send_wb_message(dict)

@app.route("/transform-dr", methods=['POST'])
def transform_dr():
    dict = create_dict_from_req(request)
    return send_dr_message(dict)


def create_dict_from_req(request):
    dict = ast.literal_eval(request.data.decode('utf-8'))
    dict = dict['message']['data']
    dict = ast.literal_eval(base64.b64decode(dict).decode('utf-8'))
    return dict

def create_wb_message(dict):
    return ping_pb2.PingStatus(service_id=dict['service_id'], timestamp=dict['timestamp'], okay=(dict['okay']==1))


def create_dr_message(dict):
    return ping_pb2.PingRequest(service_id=dict['service_id'], domain=dict['domain'])


def send_wb_message(dict):
    mess = create_wb_message(dict)
    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        return stub.AckPingStatus(mess).message
         


def send_dr_message(dict):
    mess = create_dr_message(dict)
    with grpc.secure_channel(dataretriever_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.DataRetrieverStub(channel)
        return stub.PingDomain(mess).message


if __name__ == "__main__":
    app.run()