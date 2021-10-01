import json
import os
from uuid import uuid4

from sqlmodel import col, select

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
from icon_contracts.utils.contract_content import unzip_content_to_dir
from icon_contracts.workers.kafka import Worker


class LogsWorker(Worker):
    def process_contract_creation(self):
        pass

    def java_contract(self, content, value):
        pass

    def python_contract(self, content, value):
        pass

    def process(self, msg):
        value = msg.value()

        if value.hash == "0x6d626bdfb90ea1368600956e5e57614aa29f7db7168da5ec7ddcdf87302b5640":
            print()

        print()


def logs_worker(session):
    kafka = LogsWorker(
        session=session,
        topic="logs",
        consumer_group=str(uuid4()),
    )

    kafka.start()


if __name__ == "__main__":
    from icon_contracts.workers.db import session

    logs_worker(session)
