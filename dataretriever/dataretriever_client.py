import logging
from concurrent import futures
import os
import ping_pb2
import ping_pb2_grpc
import grpc
from dotenv import load_dotenv


def run():
    with grpc.secure_channel("dataretriever-app-6oed3mtq4a-lz.a.run.app:443", grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.DataRetrieverStub(channel)

        ping_request = ping_pb2.PingRequest(domain="googleususdhaskfdsasljhdgf.com")

        ping_result = stub.PingDomain(ping_request)
        print(ping_result)
        if ping_result.okay:
            print("Ping successful:", ping_result.message)
        else:
            print("Ping failed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    run()