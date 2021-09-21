from fastapi import APIRouter
from icon_contracts.api.v1.endpoints import preps

api_router = APIRouter()
api_router.include_router(preps.router)
