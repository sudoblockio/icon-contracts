import json
from uuid import uuid4

from icon_contracts.log import logger

from icon_contracts.config import settings
from icon_contracts.workers.kafka import KafkaClient


class TransactionsWorker(KafkaClient):


    def process_contract_creation(self):
        pass


    def process(self, value):
        data = json.loads(value.data)

        if 'contentType' in data:
            pass

        if 'method' in data:
            return

        method = data['method']

        # https://www.icondev.io/references/reference-manuals/icon-contracts-score-apis#rejectscore
        if method in 'acceptScore':
            print()

        if method in 'rejectScore':
            print()

        if method in 'addAuditor':
            print()

        if method in 'removeAuditor':
            print()



def transactions_worker():
    kafka = TransactionsWorker(
        topic="transactions",
        consumer_group=str(uuid4()),
    )

    kafka.start()


if __name__ == '__main__':
    transactions_worker()
