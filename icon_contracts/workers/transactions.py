import json
import os

from uuid import uuid4
from sqlmodel import select, col

from icon_contracts.log import logger
from icon_contracts.config import settings
from icon_contracts.workers.kafka import Worker
from icon_contracts.utils.contract_content import unzip_content_to_dir
from icon_contracts.models.contracts import Contract


class TransactionsWorker(Worker):

    def process_contract_creation(self):
        pass


    def java_contract(self, content, value):
        pass

    def python_contract(self, content, value):
        contract_path = unzip_content_to_dir(content, value.hash)
        with open(os.path.join(contract_path, 'package.json')) as file:
            package_json = json.load(file)

        self.session.execute(select(Contract)).where(col(Contract.address))
        # import shutil
        # shutil.rmtree(dirpath)


    def process(self, msg):
        value = msg.value()
        # Messages are keyed by to_address
        if msg.key() == settings.GOVERNANCE_ADDRESS:
            data = json.loads(value.data)

            if 'contentType' in data:
                if data['contentType'] == 'application/zip':
                    self.python_contract(data['content'], value)

                if data['contentType'] == 'application/java':
                    self.java_contract(data['content'], value)

                print()

        # method = data['method']
        #
        # # https://www.icondev.io/references/reference-manuals/icon-contracts-score-apis#rejectscore
        # if method in 'acceptScore':
        #     print()
        #
        # if method in 'rejectScore':
        #     print()
        #
        # if method in 'addAuditor':
        #     print()
        #
        # if method in 'removeAuditor':
        #     print()


def transactions_worker(session):
    kafka = TransactionsWorker(
        session=session,
        topic="transactions",
        consumer_group=str(uuid4()),
    )

    kafka.start()


if __name__ == '__main__':
    from icon_contracts.db import session
    transactions_worker(session)
