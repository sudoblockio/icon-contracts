import binascii
import json
import os
import shutil

import pytest

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.workers.transactions import TransactionsWorker
from icon_contracts.workers.verification import get_on_chain_contract_src

source_code_link = (
    "https://berlin.tracker.solidwallet.io/score/cxdd585fff788dc1eaeb071a4cb1f18b0d76342212_1.zip"
)
owner_address = "hx9e52c40a1b26342f297e25b6f225a08fd119c8af"


def test_on_chain_contract_src():
    assert get_on_chain_contract_src(source_code_link)
    shutil.rmtree("on_chain_source_code")


def test_encoding(chdir_fixtures):
    os.chdir("java_contracts")
    with open("src.zip", "rb") as f:
        hexdata = b"0x" + binascii.hexlify(f.read())

    with open("src.txt", "w") as f:
        json.dump(hexdata.decode("utf-8"), f)

    assert hexdata.decode("utf-8").startswith("0x")


@pytest.fixture()
def clean_up_output():
    pass


@pytest.fixture()
def update_gradle_dir(base_dir):
    settings.GRADLE_PATH = os.path.join(base_dir, "docker")


@pytest.fixture()
def setup_db(db):
    contract_address = "cxdd585fff788dc1eaeb071a4cb1f18b0d76342212"
    with db as session:
        contract = session.get(Contract, contract_address)
        if contract is None:
            contract = Contract(
                address=contract_address,
                source_code_link=source_code_link,
                owner_address=owner_address,
            )
            session.add(contract)
            session.commit()


def test_process_verification(setup_db, db, update_gradle_dir, chdir_fixtures, caplog):
    os.chdir("java_contracts")
    with open("verify-schema-v1.json") as f:
        params = json.load(f)

    data = {"method": "verify", "params": params}

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

    assert "Unable verify contract" not in caplog.text
