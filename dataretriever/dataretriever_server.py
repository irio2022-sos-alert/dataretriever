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

    def __init__(self, project_id, topic_id) -> None:
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher_client = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher_client.topic_path(self.project_id, self.topic_id)


    def PingDomain(
        self, request: ping_pb2.PingRequest, context
    ) -> ping_pb2.DrStatus:
        
        response = ping(request.domain)

        if response:
            self.publish_response_data(response, request.domain)
        else:
            self.publish_response_data(0.0, request.domain, okay=0)

        return ping_pb2.DrStatus(
            okay=True,
            message=f"Ping response: {response}"
        ) 


    def publish_response_data(self, time, domain, okay=1):
        data = {"domain": domain ,"time": time, "okay": okay}
        data_json = json.dumps(data)
        send_data = str(data_json).encode("utf-8")
        logging.info(f"Data: {send_data}")
        
        self.publisher_client.publish(self.topic_path, send_data)

        # try:
        #     publisher_client.publish(topic_path, data)
        # except:
        #     logging.info(f"{self.topic_id} not found.")


def serve(port, project_id, topic_id) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_pb2_grpc.add_DataRetrieverServicer_to_server(
        DataRetrieverServicer(project_id, topic_id), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get("PORT", "50051")
    project_id = os.environ.get("PROJECT_ID")
    topic_id = os.environ.get("TOPIC_ID")

    logging.basicConfig(level=logging.INFO)
    serve(port, project_id, topic_id)