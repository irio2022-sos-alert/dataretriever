from concurrent import futures
import ping_pb2
import ping_pb2_grpc
import grpc
import os
import logging
import time
import calendar
from db import init_connection_pool, migrate_db
from models import Services, Responses
from sqlmodel import Session
from sqlalchemy import func


def get_time():
    return calendar.timegm(time.gmtime())


def get_service_window(service_id):
    with Session(engine) as session:
        return float(session.query(Services).get(service_id).alerting_window)

def check_init_service(service_id):
    with Session(engine) as session:
        if session.query(Responses).get(service_id) is None:
            timestamp = get_time()
            session.add(Responses(service_id=service_id, timestamp=timestamp))
            session.commit()


def get_service_last_available_timestamp(service_id):
    with Session(engine) as session:
        return session.query(Responses).get(service_id).timestamp

def update_service_last_available_timestamp(service_id, timestamp):
    with Session(engine) as session:
        session.query(
            Responses
        ).filter(
            Responses.service_id == service_id
        ).update(
            {Responses.timestamp: timestamp}, 
            synchronize_session=False
        )
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
        service_id, timestamp = request.service_id, request.timestamp
        check_init_service(service_id)
        last_available_timestamp = get_service_last_available_timestamp(service_id)

        logging.info(f"id: {service_id}, last available: {last_available_timestamp}, current: {request.timestamp}")

        if (last_available_timestamp > timestamp):
            logging.info(f"last timestamp higher, returning")
            return ping_pb2.WbStatus(okay=True, message="Ack")

        if request.okay:
            update_service_last_available_timestamp(service_id, timestamp)
            logging.info(f"updated last timestamp")
        else:
            alerting_window = get_service_window(service_id)
            if alerting_window is None:
                alerting_window = 50
            if (timestamp-last_available_timestamp >= alerting_window):
                logging.info(f"Alerting: {alerting_window}, {timestamp-last_available_timestamp}")
                return self.notify_alertmanager(service_id)
            else:
                logging.info(f"Not alerting yet: {alerting_window}, {timestamp-last_available_timestamp}")

        return ping_pb2.WbStatus(okay=True,message="Ack")

    def notify_alertmanager(self, service_id):
        with grpc.secure_channel(self.alertmanager_endpoint, grpc.ssl_channel_credentials()) as channel:
            mess = create_alertmanager_message(service_id)
            stub = ping_pb2_grpc.AlertManagerStub(channel)
            ping_result = stub.Alert(mess) 
            return ping_pb2.WbStatus(okay=ping_result.okay, message=ping_result.message)


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