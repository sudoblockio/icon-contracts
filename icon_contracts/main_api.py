import asyncio
from multiprocessing.pool import ThreadPool

import uvicorn
from fastapi import FastAPI
from loguru import logger
from prometheus_client import start_http_server
from starlette.middleware.cors import CORSMiddleware

from icon_contracts.api.v1.router import api_router
from icon_contracts.config import settings

tags_metadata = [
    {
        "name": "icon-contracts",
        "description": "...",
    },
]

app = FastAPI(
    title="ICON Contracts Service",
    description="...",
    version="v0.1.0",
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.DOCS_PREFIX}/openapi.json",
    docs_url=f"{settings.DOCS_PREFIX}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

logger.info("Starting application...")
app.include_router(api_router, prefix=settings.REST_PREFIX)

if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        debug=True,
        workers=1,
    )
