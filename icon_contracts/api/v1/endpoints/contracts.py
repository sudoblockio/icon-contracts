from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from icon_contracts.api.db import get_session
from icon_contracts.models.contracts import Contract

router = APIRouter()


@router.get("/contracts")
async def get_contracts(
    response: Response,
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0),
    limit: int = Query(100, gt=0, lt=101),
    contract_type: str = Query(None),
    status: str = Query(None),
) -> List[Contract]:
    """Return list of contracts"""
    query = select(Contract).offset(skip).limit(limit)
    query_count = select([func.count(Contract.address)])

    if contract_type:
        query = query.where(Contract.contract_type == contract_type)
        query_count = query_count.where(Contract.contract_type == contract_type)
    if status:
        query = query.where(Contract.status == status)
        query_count = query_count.where(Contract.status == status)

    result_count = await session.execute(query_count)
    result = await session.execute(query)

    total_count = str(result_count.scalars().all()[0])

    response.headers["x-total-count"] = total_count

    contracts = result.scalars().all()
    return contracts


@router.get("/contracts/{address}")
async def get_contract(
    address: str, session: AsyncSession = Depends(get_session)
) -> List[Contract]:
    """Return list of contracts"""
    result = await session.execute(select(Contract).where(Contract.address == address))
    contracts = result.scalars().all()

    if len(contracts) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return contracts[0]
