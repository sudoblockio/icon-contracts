from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import BIGINT, JSON, Column, Field, SQLModel

from icon_contracts.core.classifier import is_irc2
from icon_contracts.log import logger
from icon_contracts.utils.rpc import icx_call, icx_getScoreApi


class Contract(SQLModel, table=True):
    # __tablename__ = "contracts"  # type: ignore

    address: str = Field(primary_key=True)

    name: Optional[str] = Field(None, index=False)
    symbol: str = Field(None, index=False)
    decimals: str = Field(None, index=False)
    contract_type: str = Field("Contract", index=True, description="One of Contract, IRC2")

    country: Optional[str] = Field(None, index=False)
    city: Optional[str] = Field(None, index=False)
    email: Optional[str] = Field(None, index=False)
    website: Optional[str] = Field(None, index=False)
    details: Optional[str] = Field(None, index=False)

    last_updated_block: Optional[int] = Field(None, index=True)
    last_updated_timestamp: Optional[int] = Field(None, sa_column=Column(BIGINT), index=True)
    created_block: Optional[int] = Field(None, index=True)
    created_timestamp: Optional[int] = Field(None, sa_column=Column(BIGINT), index=True)

    owner_address: Optional[str] = Field(None, index=True)

    current_version: Optional[str] = Field(None, index=False)

    abi: List[dict] = Field(None, index=False, sa_column=Column(JSON))

    source_code_link: str = Field(None, index=False)
    revision_number: int = Field(
        -1,
        index=False,
        description="Out of order ID for zipped up source code in s3 "
        "/bucket/[address]_[revision_number].zip",
    )

    status: Optional[str] = Field(
        None, index=True, description="Field to inform audit status of 1.0 contracts."
    )

    is_token: Optional[bool] = Field(False, index=True)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "contracts"

    def extract_contract_details(self):
        """Get ABI and then classify contract based on that ABI."""
        response = icx_getScoreApi(address=self.address)
        if response.status_code == 200:
            self.abi = response.json()["result"]
        else:
            logger.info(f"Unknown abi for address {self.address}")
            return

        try:
            self.name = icx_call(self.address, {"method": "name"}).json()["result"]
        except Exception:
            logger.info(f"Error getting name from contract {self.address}")

        if is_irc2(self.abi, self.address):
            self.contract_type = "IRC2"
            self.symbol = icx_call(self.address, {"method": "symbol"}).json()["result"]
            self.decimals = icx_call(self.address, {"method": "decimals"}).json()["result"]
            self.is_token = True
