from multiprocessing.pool import ThreadPool
from threading import Thread

from prometheus_client import start_http_server

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.utils.contract_content import get_s3_client
from icon_contracts.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

logger.info("Starting metrics server.")

metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT + 1, settings.METRICS_ADDRESS))

s3_client = get_s3_client()

transactions_worker_head_thread = Thread(
    target=transactions_worker_head,
    args=[s3_client],
)

transactions_worker_tail_thread = Thread(
    target=transactions_worker_tail,
    args=[s3_client],
)

transactions_worker_tail_thread.start()
transactions_worker_head_thread.start()
