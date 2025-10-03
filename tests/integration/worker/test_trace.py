

from icon_contracts.workers.traces import get_intra_contract_creation_content
from icon_contracts.config import settings
from icon_contracts.workers.transactions import TransactionsWorker
from icon_contracts.schemas.block_etl_pb2 import TransactionETL


def test_get_intra_contract_creation_content():
    # 0xd90e955bfc490f2d235e407dec0288de074a5c1d0c3622c6381a1bc50609a51f

    settings.ICON_NODE_URL = "https://api.berlin.icon.community/api/v3"
    hash = "0xaeef4b72cae142dac5720fa81a7d167488bd62afde53ea4c4105c049dfe7ffd4"

    content = get_intra_contract_creation_content(hash=hash)

    print()
