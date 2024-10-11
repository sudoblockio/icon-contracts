from fastapi import APIRouter
from icon_contracts.api.v1.endpoints import contracts

api_router = APIRouter(tags=["Contracts"])
api_router.include_router(contracts.router)
