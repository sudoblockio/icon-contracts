from typing import TYPE_CHECKING

from icon_contracts.utils.rpc import getTrace
from pydantic import BaseModel, validator, ValidationError

if TYPE_CHECKING:
    from icon_contracts.workers.transactions import TransactionsWorker

ALL_BTP_CONTRACTS = {
    "berlin": [
        {
            "address": "",
            "method": "",
        },
    ]
}


class TraceLogs(BaseModel):
    msg: str
    level: int
    ts: int


class TraceResponse(BaseModel):
    status: str
    logs: list[TraceLogs]

    @validator("status")
    def validate_result(cls, v):
        if v != "0x1":
            raise ValidationError


def get_intra_contract_creation_content(hash: str):
    traces = getTrace(hash)

    if traces.status_code != 200:
        raise Exception(
            f"Could not call trace endpoint for tx hash='{hash}'")

    try:
        traces = TraceResponse(**traces.json()['result'])
    except (IndexError, ValidationError):
        raise Exception(
            f"Could decode trace for tx hash='{hash}' - {traces.json()}")

    contract_create = False
    for i_contract_create, v in enumerate(traces.logs):

        if v.msg == "FRAME[2] DEPLOY start to=cx0000000000000000000000000000000000000000":
            contract_create = True
            break

    contract_step = False
    if not contract_create:
        return
    else:
        for i, v in enumerate(traces.logs[i_contract_create + 1:]):
            if v.msg.startswith("FRAME[2] STEP apply type=contractCreate count=1"):
                found_contract_step = True
                break

    found_contract_step = False
    if not contract_step:
        return
    else:
        for i, v in enumerate(traces.logs[i + 1:]):
            if v.msg.startswith("FRAME[2] STEP apply type=contractCreate count=1"):
                found_contract_step = True
                break
