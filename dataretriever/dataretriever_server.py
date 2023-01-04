import logging
from ping3 import ping
from concurrent import futures
import dataretriever_pb2
import dataretriever_pb2_grpc
import grpc
from dotenv import load_dotenv


class DataRetrieverServicer(dataretriever_pb2_grpc.DataRetrieverServicer):
    """Provides methods that implement functionality of data retriever server."""

    def __init__(self) -> None:
        pass

    def PingDomain(
        self, request: dataretriever_pb2.PingRequest, context
    ) -> dataretriever_pb2.Status:
        response = ping(request.domain)
        print(f"Ping response: {response}")
        return dataretriever_pb2.Status(
            okay=response is not None, 
            message=""
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dataretriever_pb2_grpc.add_DataRetrieverServicer_to_server(
        DataRetrieverServicer(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    serve()