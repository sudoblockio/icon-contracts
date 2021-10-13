from multiprocessing.pool import ThreadPool
from threading import Lock, Thread

import boto3
from prometheus_client import start_http_server

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

boto3_client_lock = Lock()


def get_s3_client():
    with boto3_client_lock:
        return boto3.session.Session().client(
            "s3",
            aws_access_key_id=settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY,
        )


s3_client = get_s3_client()

logger.info("Starting metrics server.")

metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT + 1, settings.METRICS_ADDRESS))

transactions_worker_head_thread = Thread(
    target=transactions_worker_head,
    args=[],
)

transactions_worker_tail_thread = Thread(
    target=transactions_worker_tail,
    args=[s3_client],
)

transactions_worker_head_thread.start()
transactions_worker_tail_thread.start()
transactions_worker_tail_thread.join()
boto3_client_lock.join()
