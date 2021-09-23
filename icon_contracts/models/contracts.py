from __future__ import annotations

from typing import Optional, Any, List
from sqlmodel import Field, Session, SQLModel, select
from fastapi.encoders import jsonable_encoder


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
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    details: Optional[str] = None
    p2p_endpoint: Optional[str] = None
    node_address: Optional[str] = None



    def get(self, db: Session):
        return db.execute(select(Contract)).scalars().all()
