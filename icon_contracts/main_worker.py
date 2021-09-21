from threading import Thread
from multiprocessing.pool import ThreadPool

import asyncio
from loguru import logger
from prometheus_client import start_http_server

from icon_contracts.config import settings
from icon_contracts.db import init_db
from icon_contracts.workers.transactions import transactions_worker

logger.info("Starting metrics server.")
# metrics_pool = ThreadPool(1)
# metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

# asyncio.run(init_db())

transactions_worker_thread = Thread(
    target=transactions_worker,
    args=(),
)

transactions_worker_thread.daemon = True
transactions_worker_thread.start()
