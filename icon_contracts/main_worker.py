import asyncio
from multiprocessing.pool import ThreadPool
from threading import Thread

from loguru import logger
from prometheus_client import start_http_server

from icon_contracts.config import settings
from icon_contracts.db import session
from icon_contracts.workers.transactions import transactions_worker

logger.info("Starting metrics server.")


transactions_worker_thread = Thread(
    target=transactions_worker,
    args=(session),
)

transactions_worker_thread.daemon = True
transactions_worker_thread.start()
