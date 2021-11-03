import pytest

from icon_contracts.config import settings
from icon_contracts.workers.kafka import get_current_offset
from icon_contracts.workers.transactions import TransactionsWorker

PARTITION_DICT_FIXTURE = {("transactions", 0): 10000}

# def test_main(mocker, db):
#     settings.CONSUMER_GROUP = "foo"
#     mocker.patch('icon_contracts.workers.kafka.get_current_offset',
#         return_value=("test-cg", PARTITION_DICT_FIXTURE)
#     )
#     from icon_contracts import main_worker


def test_transactions_worker(db, run_process_wait):
    topic_name = "transactions"
    with db as session:
        kafka = TransactionsWorker(
            partition_dict=PARTITION_DICT_FIXTURE,
            s3_client=None,
            session=session,
            topic=topic_name,
            consumer_group="foo",
            auto_offset_reset="earliest",
        )

    run_process_wait(kafka.start, 5)


# def test_get_offset_per_partition(db):
#     topic_name = "test"
#     with db as session:
#         kafka = TransactionsWorker(
#             partition_dict=PARTITION_DICT_FIXTURE,
#             s3_client=None,
#             session=session,
#             topic=topic_name,
#             consumer_group="foo",
#             auto_offset_reset="earliest",
#         )
#     partitions = kafka.get_offset_per_partition()
#
#     offset = [i.offset for i in kafka.get_offset_per_partition() if i.partition == 0]
#
#     assert len(partitions) == 12
#
#     kafka.start()
