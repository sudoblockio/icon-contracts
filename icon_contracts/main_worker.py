from contextlib import ExitStack
from multiprocessing.pool import ThreadPool
from threading import Lock, Thread

import boto3
from prometheus_client import start_http_server
from sqlalchemy.orm import scoped_session

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.workers.db import session_factory
from icon_contracts.workers.kafka import get_current_offset
from icon_contracts.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

boto3_client_lock = Lock()


def get_s3_client():
    # We need to share the client across threads due to botocore#1246
    if settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID is not None:
        logger.info(f"Init s3 client to upload zipped contracts.")
        with boto3_client_lock:
            return boto3.session.Session().client(
                "s3",
                aws_access_key_id=settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY,
            )
    else:
        logger.info(f"Missing credentials for s3 client to upload zipped contracts.")
        return None


s3_client = get_s3_client()

logger.info("Starting metrics server.")

metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT + 1, settings.METRICS_ADDRESS))

Session = scoped_session(session_factory)
job_init_session = Session()

consumer_group, partition_dict = get_current_offset(job_init_session)

with ExitStack() as stack:
    Session = scoped_session(session_factory)

    transactions_worker_head_session = Session()
    transactions_worker_head_thread = Thread(
        target=transactions_worker_head,
        args=(
            transactions_worker_head_session,
            s3_client,
            consumer_group,
        ),
    )
    transactions_worker_head_thread.start()

    if partition_dict is not None:
        # Partition list will be None when it is not supplied by the `kafka_jobs`
        # table which should exist in the DB and populated by an init container before
        # the service initializes.
        transactions_worker_tail_session = Session()
        transactions_worker_tail_thread = Thread(
            target=transactions_worker_tail,
            args=(transactions_worker_tail_session, s3_client, consumer_group, partition_dict),
        )
        transactions_worker_tail_thread.start()
