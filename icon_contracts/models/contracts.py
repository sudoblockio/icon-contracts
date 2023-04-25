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
from icon_contracts.utils.rpc import (
    getScoreStatus,
    getTransactionByHash,
    icx_call,
    icx_getScoreApi,
    make_call,
)


class Contract(SQLModel, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str] = Field(None, index=False)
    symbol: str = Field(None, index=False)
    decimals: str = Field(None, index=False)

    contract_type: str = Field(None, index=True, description="One of python / java")
    token_standard: str = Field(None, index=True, description="One of Contract, IRC2")

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

    audit_tx_hash: str = Field(None, index=False)
    code_hash: str = Field(None, index=False)
    deploy_tx_hash: str = Field(None, index=False)

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
            logger.debug(f"Unknown abi for address {self.address}")
            return

        try:
            self.name = icx_call(self.address, {"method": "name"}).json()["result"]
        except Exception:
            logger.debug(f"Error getting name from contract {self.address}")

        try:
            self.symbol = icx_call(self.address, {"method": "symbol"}).json()["result"]
        except Exception:
            logger.debug(f"Error getting symbol from contract {self.address}")

        try:
            self.decimals = icx_call(self.address, {"method": "decimals"}).json()["result"]
        except Exception:
            logger.debug(f"Error getting decimals from contract {self.address}")

        # IRC 2
        if contract_classifier(self.abi, IRC2_METHODS):
            self.token_standard = "irc2"
            try:
                self.symbol = icx_call(self.address, {"method": "symbol"})
            except Exception:
                logger.info(f"symbol missing in classified contract {self.address}")
            try:
                self.decimals = make_call(icx_call(self.address, {"method": "decimals"}))
            except Exception:
                logger.info(f"decimals missing in classified contract {self.address}")
            self.is_token = True

        # IRC 3
        elif contract_classifier(self.abi, IRC3_METHODS):
            self.token_standard = "irc3"
            self.is_token = True
            self.is_nft = True

        # IRC 31
        elif contract_classifier(self.abi, IRC31_METHODS):
            self.token_standard = "irc31"
            self.is_token = True
            self.is_nft = True

        r = getScoreStatus(address=self.address)
        if r.status_code == 200:
            score_status = r.json()["result"]

            try:
                if "current" in score_status:
                    # The cx0 address only has these three values
                    self.contract_type = score_status["current"]["type"]
                    self.status = score_status["current"]["status"].capitalize()
                    self.code_hash = score_status["current"]["codeHash"]
                    # Most others have these
                    self.owner_address = score_status["owner"]
                    self.audit_tx_hash = score_status["current"]["auditTxHash"]
                    self.deploy_tx_hash = score_status["current"]["deployTxHash"]
                else:
                    logger.info(f"score status not available in {self.address}")
            except (IndexError, KeyError) as e:
                logger.info(f"Error getting status - {e} \naddress={self.address}")

        if self.creation_hash is not None:
            # Creation hash does not come from RPC, rather stream processing and can include
            # an earlier date than the RPC.
            hash = self.creation_hash
        else:
            # Sometimes stream processing doesn't have data so as a back up we use RPC
            hash = self.deploy_tx_hash

        r = getTransactionByHash(hash)
        if r.status_code != 200:
            logger.debug(f"Invalid scoreStatus response for address={self.address}")
        else:
            tx_result = r.json()["result"]
            self.created_timestamp = int(tx_result["timestamp"], 0)
            self.created_block = int(tx_result["blockHeight"], 0)
