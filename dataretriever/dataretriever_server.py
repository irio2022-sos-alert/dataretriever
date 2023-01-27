from ping3 import ping
from concurrent import futures
import logging
import ping_pb2
import ping_pb2_grpc
import grpc
import os
from google.cloud import pubsub_v1
import json

# _PORT = os.environ["PORT"]

class DataRetrieverServicer(ping_pb2_grpc.DataRetrieverServicer):
    """Provides methods that implement functionality of data retriever server."""

    def __init__(self, whistleblower_endpoint, project_id, topic_id) -> None:
        self.x = 0
        self.whistleblower_endpoint = whistleblower_endpoint
        self.project_id = project_id
        self.topic_id = topic_id


    def PingDomain(
        self, request: ping_pb2.PingRequest, context
    ) -> ping_pb2.DrStatus:
        
        response = ping(request.domain)
        self.x += 1

        if response:
            self.publish_response_data(response, request.domain)
        else:
            self.publish_response_data(0.0, request.domain, okay=1)

        return ping_pb2.DrStatus(
            okay=True,
            message=f"Ping response: {response}, count: {self.x}"
        ) 


    def publish_response_data(self, time, domain, okay=0):
        publisher_client = pubsub_v1.PublisherClient()
        topic_path = publisher_client.topic_path(self.project_id, self.topic_id)

        data = {"domain": domain ,"time": time, "okay": okay}
        data_json = json.dumps(data)
        send_data = str(data_json).encode("utf-8")
        logging.info(f"Data: {send_data}")
        
        publisher_client.publish(topic_path, send_data)

        # try:
        #     publisher_client.publish(topic_path, data)
        # except:
        #     logging.info(f"{self.topic_id} not found.")


def serve(port, whistleblower_endpoint, project_id, topic_id) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_pb2_grpc.add_DataRetrieverServicer_to_server(
        DataRetrieverServicer(whistleblower_endpoint, project_id, topic_id), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get("PORT", "50051")
    whistleblower_endpoint = os.environ.get("WHISTLEBLOWER_ENDPOINT", "[::]:50052")
    project_id = os.environ.get("PROJECT_ID", "cloud-run-grpc-ping")
    topic_id = os.environ.get("TOPIC_ID", "whistleblower-topic")

    logging.basicConfig(level=logging.INFO)
    serve(port, whistleblower_endpoint, project_id, topic_id)