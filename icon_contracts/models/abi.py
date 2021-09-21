from typing import Optional, Any, List
from sqlmodel import Field, Session, SQLModel, create_engine


class ABIBase(SQLModel):
    address: str
    block_height: str
    abi: List[dict]


class ABIBlocks(ABIBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ABIsBase(SQLModel):
    address: str
    prep_address: str
    amount: str
