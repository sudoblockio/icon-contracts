import pytest

from icon_contracts.config import settings
from icon_contracts.workers.kafka import get_current_offset

PARTITION_DICT_FIXTURE = {("transactions", 0): 10000}


@pytest.fixture()
def backfill_job(db):
    def f(job_id):
        with db as session:
            sql = "DROP TABLE IF EXISTS kafka_jobs;"
            session.execute(sql)
            session.commit()

            sql = "CREATE TABLE IF NOT EXISTS kafka_jobs (job_id varchar, worker_group varchar, topic varchar, partition bigint, stop_offset bigint, PRIMARY KEY (job_id, worker_group, topic, partition));"
            session.execute(sql)
            session.commit()

            num_msgs = 1000
            for i in range(0, 12):
                sql = (
                    f"INSERT INTO kafka_jobs (job_id, worker_group, topic, partition, stop_offset) VALUES "
                    f"('{job_id}','{settings.CONSUMER_GROUP}-{job_id}',"
                    f"'{settings.CONSUMER_TOPIC_BLOCKS}','{i}','{num_msgs}');"
                )
                session.execute(sql)
                session.commit()

    return f
    # yield


def test_get_current_offset(db, backfill_job):
    settings.JOB_ID = "test6"
    backfill_job(settings.JOB_ID)

    with db as session:
        consumer_group, partition_dict = get_current_offset(session)

    assert consumer_group
    assert partition_dict[("blocks", 0)] == 1000


# def test_transactions_worker_tail(db, backfill_job):
#     import random
#     import string
#     # settings.JOB_ID = "test3"
#     settings.JOB_ID = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
#     backfill_job(settings.JOB_ID)
#
#     with db as session:
#         consumer_group, partition_dict = get_current_offset(session)
#
#     from icon_contracts.workers.transactions import transactions_worker_tail
#
#     transactions_worker_tail(
#         consumer_group=consumer_group,
#         partition_dict=partition_dict,
#     )


# def test_transactions_worker(db, backfill_job, run_process_wait):
#     topic_name = "transactions"
#     with db as session:
#         consumer_group, partition_dict = get_current_offset(session)
#         kafka = TransactionsWorker(
#             partition_dict=partition_dict,
#             s3_client=None,
#             session=session,
#             topic=topic_name,
#             consumer_group=consumer_group,
#             auto_offset_reset="earliest",
#         )
#         kafka.start()
#         run_process_wait(kafka.start(), 5)

# run_process_wait(kafka.start, 5)


# def test_main(mocker, db):
#     settings.CONSUMER_GROUP = "foo"
#     mocker.patch('icon_contracts.workers.kafka.get_current_offset',
#         return_value=("test-cg", PARTITION_DICT_FIXTURE)
#     )
#     from icon_contracts import main_worker


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
