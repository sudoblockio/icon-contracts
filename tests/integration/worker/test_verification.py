import binascii
import json
import os
import shutil

import pytest

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
from icon_contracts.models.social_media import SocialMedia
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.workers.transactions import TransactionsWorker
from icon_contracts.workers.verification import get_on_chain_contract_src

contract_address = "cx0744c46c005f254e512ae6b60aacd0a9b06eda1f"
source_code_link = (
    # f"https://berlin.tracker.solidwallet.io/score/{contract_address}.zip"
    f"https://icon-explorer-prod.s3.us-west-2.amazonaws.com/contract-sources/{contract_address}_1"
)
owner_address = "hx37844fad06ed32738e754b205c747430a7feb81e"


def test_on_chain_contract_src():
    assert get_on_chain_contract_src(source_code_link)
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
    with db as session:
        contract = session.get(Contract, contract_address)
        contract.source_code_link = (source_code_link,)
        contract.owner_address = (owner_address,)
        session.add(contract)
        session.commit()


def test_process_verification(setup_db, db, update_gradle_dir, chdir_fixtures, caplog):
    """
    Validate the contract verification process by populating DB with a source code link
    and processing a transaction with a protobuf fixture.
    """
    os.chdir("java_contracts")
    with open("verify-schema-v1.json") as f:
        params = json.load(f)

    data = {"method": "verify", "params": params}

    # Create a proto
    tx = TransactionRaw(
        hash="foo",
        data=json.dumps(data),
        from_address=owner_address,
    )

    with db as session:
        tx_worker = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
            consumer_group="foo",
            auto_offset_reset="earliest",
            check_topics=False,
        )
        tx_worker.process_verification(value=tx)

        social_media = session.get(SocialMedia, params["contract_address"])

    assert social_media.country == "space"
    assert "Unable verify contract" not in caplog.text
    assert "Successfully compared" in caplog.text
