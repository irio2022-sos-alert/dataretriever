from ping3 import ping
from concurrent import futures
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
import os
from google.cloud import pubsub_v1

# _PORT = os.environ["PORT"]

class DataRetrieverServicer(ping_pb2_grpc.DataRetrieverServicer):
    """Provides methods that implement functionality of data retriever server."""

    def __init__(self, whistleblower_endpoint) -> None:
        self.x = 0
        self.whistleblower_endpoint = whistleblower_endpoint

    def PingDomain(
        self, request: ping_pb2.PingRequest, context
    ) -> ping_pb2.Status:
        
        response = ping(request.domain)
        calculated_sum = self.call_service(response)
        self.x += 1

        return ping_pb2.Status(
            okay=True,
            message=f"Ping response: {response}, Sum: {calculated_sum}, count: {self.x}"
        ) 

    # def publish_response_data():
    #     publisher = pubsub_v1.PublisherClient()
    #     topic_name = 'projects/cloud-run-grpc-ping/topics/ping-responses'
    #     publisher.create_topic(name=topic_name)
    #     future = publisher.publish(topic_name, b'My first message!', spam='eggs')
    #     future.result()

    def call_service(self, time):
        with grpc.secure_channel("whistleblower-app-6oed3mtq4a-lz.a.run.app", grpc.ssl_channel_credentials()) as channel:
            stub = ping_pb2_grpc.WhistleblowerStub(channel)

            sum_request = ping_pb2.CalculateSum(domain="google.com", time=time)

            ping_result = stub.SumResponseTimes(sum_request)
            
            return ping_result.sum

def serve(port, whistleblower_endpoint) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_pb2_grpc.add_DataRetrieverServicer_to_server(
        DataRetrieverServicer(whistleblower_endpoint), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get("PORT", "50051")
    whistleblower_endpoint = os.environ.get("WHISTLEBLOWER_ENDPOINT", "[::]:50052")
    logging.basicConfig(level=logging.INFO)
    serve(port, whistleblower_endpoint)