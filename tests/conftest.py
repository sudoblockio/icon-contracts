import logging
import os
from typing import Generator

import pytest
from _pytest.logging import caplog as _caplog
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy.orm import sessionmaker

from icon_contracts.main_api import app
from icon_contracts.workers.db import engine

# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()


@pytest.fixture(scope="session")
def db():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def caplog(_caplog):
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)


@pytest.fixture
def fixtures_dir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "fixtures")
