from threading import Thread
from multiprocessing.pool import ThreadPool
import asyncio
from loguru import logger
from prometheus_client import start_http_server
from icon_contracts.config import settings

from icon_contracts.workers.transactions import transactions_worker
# from icon_contracts.db import SQLALCHEMY_DATABASE_URL
# from sqlmodel import create_engine
# from sqlalchemy.orm import sessionmaker
# import psycopg2

from icon_contracts.db import session

logger.info("Starting metrics server.")


transactions_worker_thread = Thread(
    target=transactions_worker,
    args=(session),
)

transactions_worker_thread.daemon = True
transactions_worker_thread.start()
