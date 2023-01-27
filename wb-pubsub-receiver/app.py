import os
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
from flask import Flask, request
from gcp_logging import GCPHandler

app = Flask(__name__)


g = GCPHandler(app, parentLogName="parent",
    childLogName="child",
    traceHeaderName='X-Cloud-Trace-Context',
    labels= {'foo': 'bar', 'baz': 'qux'},
    resource='global')

g.setLevel(logging.INFO)
app.logger.addHandler(g)


@app.before_first_request
def init():
    global project_id, topic_id, whistleblower_endpoint
    project_id = "cloud-run-grpc-ping"
    topic_id = "whistleblower-topic"
    whistleblower_endpoint = "whistleblower-app-6oed3mtq4a-lz.a.run.app"


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
    print("test print")
    app.logger.info("test info logger")
    with grpc.secure_channel(whistleblower_endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)
        ping_result = stub.SumResponseTimes(mess)


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    app.run()