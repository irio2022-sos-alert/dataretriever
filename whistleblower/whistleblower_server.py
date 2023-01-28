from concurrent import futures
import ping_pb2
import ping_pb2_grpc
import grpc
import os
import logging
from db import init_connection_pool, migrate_db
# from models import Services, Responses
from sqlmodel import Session


def get_service_window(service_id):
    return {"alerting-window": 15.0}


def get_service_last_available_timestamp(service_id):
    pass

def update_service_last_available_timestamp(service_id, timestamp):
    pass

def create_alertmanager_message(service_id):
    pass


class WhistleblowerServicer(ping_pb2_grpc.WhistleblowerServicer):
    """Provides methods that implement functionality of whistleblower server."""

    def __init__(self, alertmanager_endpoint) -> None:
        self.alertmanager_endpoint = alertmanager_endpoint

    def AckPingStatus(
        self, request: ping_pb2.PingStatus, context
    ) -> ping_pb2.WbStatus:
        service_id, timestamp = request.service_id, request.timestamp
        last_available_timestamp = get_service_last_available_timestamp(service_id)

        if (last_available_timestamp > timestamp):
            return

        if request.okay:
            update_service_last_available_timestamp(service_id, timestamp)
        else:
            alerting_window = get_service_window(service_id)
            if (timestamp-last_available_timestamp >= alerting_window):
                self.notify_alertmanager(service_id)

        return ping_pb2.WbStatus(
            okay=True,
            message="Ack"
        )

    def notify_alertmanager(self, service_id):
        with grpc.secure_channel(self.alertmanager_endpoint, grpc.ssl_channel_credentials()) as channel:
            mess = create_alertmanager_message(service_id)
            stub = ping_pb2_grpc.DataRetrieverStub(channel)
            # ping_result = stub.PingDomain(mess)

def init_db():
    global engine
    engine = init_connection_pool()
    migrate_db(engine)


def serve(port, alertmanager_endpoint) -> None:
    init_db()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_pb2_grpc.add_WhistleblowerServicer_to_server(
        WhistleblowerServicer(alertmanager_endpoint), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = os.environ.get("PORT", "50052")
    alertmanager_endpoint = os.environ.get("ALERTMANAGER_ENDPOINT")
    serve(port, alertmanager_endpoint)