import logging
from concurrent import futures
import os
import ping_pb2
import ping_pb2_grpc
import grpc
from dotenv import load_dotenv
import time

def create_alertmanager_message(service_id):
    return ping_pb2.AlertRequest(serviceId=service_id)

def run():
    # with grpc.secure_channel("whistleblower-app-2xieibhnsq-lz.a.run.app", grpc.ssl_channel_credentials()) as channel:
    #     stub = ping_pb2_grpc.WhistleblowerStub(channel)

    #     ping_request = ping_pb2.PingStatus(service_id=1, timestamp=time.time(), okay=True)

    #     ping_result = stub.AckPingStatus(ping_request)
    #     print(ping_result)
    #     if ping_result.okay:
    #         print("Ping successful:", ping_result.message)
    #     else:
    #         print("Ping failed")
    with grpc.secure_channel("alertmanager-2xieibhnsq-lz.a.run.app", grpc.ssl_channel_credentials()) as channel:
            mess = create_alertmanager_message(1)
            stub = ping_pb2_grpc.AlertManagerStub(channel)
            ping_result = stub.Alert(mess)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    run()