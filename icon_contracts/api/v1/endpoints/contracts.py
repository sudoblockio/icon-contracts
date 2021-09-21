from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import Field, Session, SQLModel, create_engine, select

from typing import List

from icon_contracts.db import get_session
from icon_contracts.models.contracts import Contract

router = APIRouter()


@router.get("/contracts")
async def get_contracts(
        session: AsyncSession = Depends(get_session)) -> List[Contract]:
    """Return list of contracts"""
    result = await session.execute(select(Contract))
    contracts = result.scalars().all()
    return contracts
