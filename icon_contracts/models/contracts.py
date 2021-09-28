from __future__ import annotations

from typing import Any, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlmodel import Field, Session, SQLModel, select


class ContractBase(SQLModel):
    address: str
    name: str = None
    country: str = None
    city: str = None
    email: str = None
    website: str = None
    details: str = None
    p2p_endpoint: str = None
    node_address: str = None


class ContractCreate(ContractBase):
    pass


class Contract(SQLModel, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    details: Optional[str] = None
    p2p_endpoint: Optional[str] = None
    node_address: Optional[str] = None

    last_updated_block: Optional[int]
    last_updated_timestamp: Optional[int]
    created_block: Optional[int] = None
    created_timestamp: Optional[int] = None

    current_version: Optional[str] = None

    status: Optional[str] = Field(
        None, description="Field to inform audit status of 1.0 contracts."
    )

    def get(self, db: Session):
        return db.execute(select(Contract)).scalars().all()
