from prometheus_client import start_http_server

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.workers.db import engine, session_factory
from icon_contracts.workers.kafka import get_current_offset
from icon_contracts.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

logger.info("Starting metrics server.")

start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

if not settings.IS_TAIL_WORKER:
    logger.info("Worker is a head worker...")
    transactions_worker_head(
        consumer_group=settings.CONSUMER_GROUP,
    )

else:
    logger.info("Worker is a backfill worker...")
    # Partition list is supplied by the `kafka_jobs` table which should exist in
    # the DB and populated by an init container before the service initializes.
    with session_factory(bind=engine) as session:
        consumer_group, partition_dict = get_current_offset(session)

    transactions_worker_tail(consumer_group=consumer_group, partition_dict=partition_dict)
