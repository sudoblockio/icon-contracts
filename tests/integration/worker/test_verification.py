import binascii
import json
import os
import shutil

import pytest

from icon_contracts.config import settings
from icon_contracts.models.contracts import Contract
from icon_contracts.models.social_media import SocialMedia

# from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.schemas.block_etl_pb2 import BlockETL, TransactionETL
from icon_contracts.workers.transactions import TransactionsWorker
from icon_contracts.workers.verification import get_on_chain_contract_src


def test_on_chain_contract_src():
    assert get_on_chain_contract_src(
        "https://icon-contracts-s3-bucket-prod-v2.s3.us-west-2.amazonaws.com/contract-sources/cx001324aa02bee31b374a9973d044818925e06db5_0"
    )
    shutil.rmtree("on_chain_source_code")


def test_encoding(chdir_fixtures):
    os.chdir("java_contracts")
    with open("src.zip", "rb") as f:
        hexdata = b"0x" + binascii.hexlify(f.read())

    with open("src.txt", "w") as f:
        json.dump(hexdata.decode("utf-8"), f)

    os.remove("src.txt")

    assert hexdata.decode("utf-8").startswith("0x")


@pytest.fixture()
def update_gradle_dir(base_dir):
    settings.GRADLE_PATH = os.path.join(base_dir, "docker")


@pytest.fixture()
def setup_db(db):
    def f(contract_address, source_code_link, owner_address):
        with db as session:
            contract = session.get(Contract, contract_address)
            if contract is None:
                contract = Contract()
            contract.address = contract_address
            contract.source_code_link = source_code_link
            contract.owner_address = owner_address
            session.add(contract)
            session.commit()

    return f


@pytest.mark.parametrize(
    "tx_fixture,contract_address,source_code_link,owner_address",
    [
        (
            "zip-source-v1.json",
            "cx0744c46c005f254e512ae6b60aacd0a9b06eda1f",  # cx_addresss
            "https://icon-contracts-s3-bucket-prod-v2.s3.us-west-2.amazonaws.com/contract-sources/cx0744c46c005f254e512ae6b60aacd0a9b06eda1f_1",
            "hx37844fad06ed32738e754b205c747430a7feb81e",
        ),
        # (
        #     "github-source-v1.json",
        #     "cxb1e02f2bedcb3a1ad5ee913f3b7c895511f19d1c",  # cx_addresss
        #     "https://icon-explorer-prod.s3.us-west-2.amazonaws.com/contract-sources/cxb1e02f2bedcb3a1ad5ee913f3b7c895511f19d1c_1",
        #     "hx61b3ad6db9eb3e8e3c369187bffdc584227d21ed",
        # ),
    ],
)
def test_process_verification(
    tx_fixture,
    contract_address,
    source_code_link,
    owner_address,
    setup_db,
    db,
    update_gradle_dir,
    chdir_fixtures,
    caplog,
):
    """
    Validate the contract verification process by populating DB with a source code link
    and processing a transaction with a protobuf fixture.
    """
    setup_db(contract_address, source_code_link, owner_address)
    os.chdir("java_contracts")
    with open(tx_fixture) as f:
        params = json.load(f)

    data = {"method": "verify", "params": params}

    # Create a proto
    block = BlockETL(
        number=10000,
    )
    tx = TransactionETL(
        hash="foo",
        data=json.dumps(data),
        from_address=owner_address,
    )

    with db as session:
        tx_worker = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_BLOCKS,
            consumer_group="foo",
            auto_offset_reset="earliest",
            check_topics=False,
        )
        tx_worker.block = block
        tx_worker.transaction = tx
        tx_worker.process_verification()

        social_media = session.get(SocialMedia, params["contract_address"])

    assert social_media.country == "space"
    assert "Unable verify contract" not in caplog.text
    assert "Successfully compared" in caplog.text
