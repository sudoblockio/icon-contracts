import logging

from _pytest.logging import caplog as _caplog
from loguru import logger

from typing import Generator
import pytest
from fastapi.testclient import TestClient
from icon_contracts.db import get_session
from icon_contracts.main_api import app


# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()


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
