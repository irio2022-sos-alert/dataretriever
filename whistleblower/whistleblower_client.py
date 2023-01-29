import logging
from concurrent import futures
import os
import ping_pb2
import ping_pb2_grpc
import grpc
from dotenv import load_dotenv
import time


def run():
    with grpc.secure_channel("whistleblower-app-2xieibhnsq-lz.a.run.app", grpc.ssl_channel_credentials()) as channel:
        stub = ping_pb2_grpc.WhistleblowerStub(channel)

        ping_request = ping_pb2.PingStatus(service_id=1, timestamp=time.time(), okay=False)

        ping_result = stub.AckPingStatus(ping_request)
        print(ping_result)
        if ping_result.okay:
            print("Ping successful:", ping_result.message)
        else:
            print("Ping failed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    run()