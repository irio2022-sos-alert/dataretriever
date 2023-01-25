import logging
from concurrent import futures
import os
import ping_pb2
import ping_pb2_grpc
import grpc
from dotenv import load_dotenv


def run():
    with grpc.secure_channel("dataretriever-app-6oed3mtq4a-lz.a.run.app", grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.DataRetrieverStub(channel)

        ping_request = ping_pb2.PingRequest(domain="google.com")

        ping_result = stub.PingDomain(ping_request)
        if ping_result.okay:
            print("Ping successful")
        else:
            print("Ping failed")


if __name__ == "__main__":
    load_dotenv()
    run()