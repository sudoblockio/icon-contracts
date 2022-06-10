from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import BIGINT, JSON, Column, Field, SQLModel

from icon_contracts.core import (
    IRC2_METHODS,
    IRC3_METHODS,
    IRC31_METHODS,
    contract_classifier,
)
from icon_contracts.log import logger
from icon_contracts.utils.rpc import icx_call, icx_getScoreApi


class Contract(SQLModel, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str] = Field(None, index=False)
    symbol: str = Field(None, index=False)
    decimals: str = Field(None, index=False)
    contract_type: str = Field("Contract", index=True, description="One of Contract, IRC2")

    email: Optional[str] = Field(None, index=False)
    website: Optional[str] = Field(None, index=False)

    last_updated_block: Optional[int] = Field(None, index=True)
    last_updated_timestamp: Optional[int] = Field(None, sa_column=Column(BIGINT), index=True)
    created_block: Optional[int] = Field(None, index=True)
    created_timestamp: Optional[int] = Field(None, sa_column=Column(BIGINT), index=True)
    creation_hash: Optional[str] = Field(None, index=False)

    owner_address: Optional[str] = Field(None, index=False)

    current_version: Optional[str] = Field(None, index=False)

    abi: List[dict] = Field(None, index=False, sa_column=Column(JSON))

    source_code_link: str = Field(None, index=False)
    verified_source_code_link: str = Field(None, index=False)
    verified: bool = Field(False, index=True)
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
    is_nft: Optional[bool] = Field(False, index=True)

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

        # IRC 2
        if contract_classifier(self.abi, IRC2_METHODS):
            self.contract_type = "IRC2"
            self.symbol = icx_call(self.address, {"method": "symbol"}).json()["result"]
            self.decimals = icx_call(self.address, {"method": "decimals"}).json()["result"]
            self.is_token = True

        # IRC 3
        if contract_classifier(self.abi, IRC3_METHODS):
            self.contract_type = "IRC3"
            self.is_token = True
            self.is_nft = True

        # IRC 31
        if contract_classifier(self.abi, IRC31_METHODS):
            self.contract_type = "IRC31"
            self.is_token = True
            self.is_nft = True
