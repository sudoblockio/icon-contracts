import os

from icon_contracts.config import settings
from icon_contracts.utils.contract_content import upload_to_s3

# def test_upload_to_s3(load_environment_variables):
#     settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID = os.getenv('CONTRACTS_S3_AWS_ACCESS_KEY_ID')
#     settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY = os.getenv('CONTRACTS_S3_AWS_SECRET_ACCESS_KEY')
#     settings.CONTRACTS_S3_BUCKET = os.getenv('CONTRACTS_S3_BUCKET')
#
#     upload_to_s3(filename="Makefile", key="foo")
