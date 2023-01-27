from concurrent import futures
import ping_pb2
import ping_pb2_grpc
import grpc
import os
import logging

# _PORT = os.environ["PORT"]

class WhistleblowerServicer(ping_pb2_grpc.WhistleblowerServicer):
    """Provides methods that implement functionality of whistleblower server."""

    def __init__(self) -> None:
        pass

    def SumResponseTimes(
        self, request: ping_pb2.CalculateSum, context
    ) -> ping_pb2.RetSum:
        logging.info(f"Request time: {request.time}")
        logging.info(f"Request domain: {request.domain}")
        return ping_pb2.RetSum(
            okay=True,
            sum=request.time + 1.0
        )


def serve(port) -> None:
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