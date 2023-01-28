from concurrent import futures
import ping_pb2
import ping_pb2_grpc
import grpc
import os
import logging
import time
from db import init_connection_pool, migrate_db
from models import Services, Responses
from sqlmodel import Session
from sqlalchemy import func


def init_mock_service():
    with Session(engine) as session:
        if session.query(Services).all() == []:
            session.add(Services(
                id=1,
                name="test",
                domain="google.com",
                frequency=5,
                alerting_window=50,
                allowed_response_time=50
            ))
            session.commit()


def get_service_window(service_id):
    with Session(engine) as session:
        return float(session.query(Services).get(service_id).alerting_window)

def check_init_service(service_id):
    with Session(engine) as session:
        if session.query(Responses).get(service_id) is None:
            timestamp = int(time.time())
            session.add(Responses(service_id=service_id, timestamp=timestamp))
            session.commit()


def get_service_last_available_timestamp(service_id):
    with Session(engine) as session:
        return session.query(Responses).get(service_id).timestamp

def update_service_last_available_timestamp(service_id):
    timestamp = int(time.time())
    with Session(engine) as session:
        session.query(
            Responses
        ).filter(
            Responses.service_id == service_id
        ).update({Responses.timestamp: timestamp}, synchronize_session=False)
        session.commit()

def create_alertmanager_message(service_id):
    return ping_pb2.AlertRequest(serviceId=service_id)


class WhistleblowerServicer(ping_pb2_grpc.WhistleblowerServicer):
    """Provides methods that implement functionality of whistleblower server."""

    def __init__(self, alertmanager_endpoint) -> None:
        self.alertmanager_endpoint = alertmanager_endpoint

    def AckPingStatus(
        self, request: ping_pb2.PingStatus, context
    ) -> ping_pb2.WbStatus:
        init_mock_service()
        service_id, timestamp = request.service_id, int(request.timestamp)
        check_init_service(service_id)
        last_available_timestamp = get_service_last_available_timestamp(service_id)

        logging.info(f"last available: {last_available_timestamp}, current: {request.timestamp}")

        if (last_available_timestamp > timestamp):
            return

        if request.okay:
            update_service_last_available_timestamp(service_id)
        else:
            alerting_window = get_service_window(service_id)
            if alerting_window is None:
                alerting_window = 50
            if (timestamp-last_available_timestamp >= alerting_window):
                logging.info(f"Alerting: {alerting_window}, {timestamp-last_available_timestamp}")
                self.notify_alertmanager(service_id)
            else:
                logging.info(f"Alerting: {alerting_window}, {timestamp-last_available_timestamp}")

        logging.info(f"returning")
        return ping_pb2.WbStatus(
            okay=True,
            message="Ack"
        )

    def notify_alertmanager(self, service_id):
        with grpc.secure_channel(self.alertmanager_endpoint, grpc.ssl_channel_credentials()) as channel:
            mess = create_alertmanager_message(service_id)
            stub = ping_pb2_grpc.AlertManagerStub(channel)
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