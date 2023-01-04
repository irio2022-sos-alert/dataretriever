import logging
from concurrent import futures
import os
import dataretriever_pb2
import dataretriever_pb2_grpc
import grpc
from dotenv import load_dotenv
from google.cloud import pubsub_v1
    
def run(subscription_path: str, publishing_path: str):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = dataretriever_pb2_grpc.DataRetrieverStub(channel)

        subscriber = None #pubsub_v1.SubscriberClient()
        publisher = None #pubsub_v1.PublisherClient()

        # streaming_pull_future = subscriber.subscribe(
        #     subscription_path, 
        #     callback = callback_creator(publisher, publishing_path, stub)
        # )

        # with subscriber:
        #     try:
        #         streaming_pull_future.result()
        #     except pubsub_v1.TimeoutError:
        #         streaming_pull_future.cancel()
        #         streaming_pull_future.result()

        cb = callback_creator(publisher, publishing_path, stub)
        cb("google.com")

def callback_creator(publisher, publishing_path, stub):
    def callback(msg):
        ping_request = dataretriever_pb2.PingRequest(domain=msg)

        ping_result = stub.PingDomain(ping_request)
        if ping_result.okay:
            # publisher.publish(publishing_path, msg)
            print("Ping successful")
        else:
            print("Ping failed")
    return callback

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    subscription_path = "" # os.environ.get('SUBSCRIPTION_PATH')
    publishing_path = "" #os.environ.get('PUBLISHING_PATH')
    run(subscription_path, publishing_path)