from concurrent import futures
import ping_pb2
import ping_pb2_grpc
import grpc
import os
import logging
from db import init_connection_pool, migrate_db
from models import Services, Responses
from sqlmodel import Session


# _PORT = os.environ["PORT"]

class WhistleblowerServicer(ping_pb2_grpc.WhistleblowerServicer):
    """Provides methods that implement functionality of whistleblower server."""

    def __init__(self) -> None:
        pass

    def AckPingStatus(
        self, request: ping_pb2.PingStatus, context
    ) -> ping_pb2.WbStatus:
        logging.info(f"Request time: {request.time}")
        logging.info(f"Request domain: {request.domain}")
        logging.info(f"Request okay: {request.okay}")
        return ping_pb2.WbStatus(
            okay=True,
            message="Ack"
        )


def init_db():
    global engine
    engine = init_connection_pool()
    migrate_db(engine)


def serve(port) -> None:
    init_db()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_pb2_grpc.add_WhistleblowerServicer_to_server(
        WhistleblowerServicer(), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = os.environ.get("PORT", "50052")
    serve(port)