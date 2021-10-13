import os

from icon_contracts.config import settings
from icon_contracts.workers.transactions import transactions_worker_tail

# def test_transactions_worker_tail(load_environment_variables, run_process_wait):
#     settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID = os.getenv('CONTRACTS_S3_AWS_ACCESS_KEY_ID')
#     settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY = os.getenv('CONTRACTS_S3_AWS_SECRET_ACCESS_KEY')
#     settings.CONTRACTS_S3_BUCKET = os.getenv('CONTRACTS_S3_BUCKET')
#     from icon_contracts import main_worker
#     run_process_wait(transactions_worker_tail(), 10)
