from icon_contracts.models.contracts import Contract
from sqlmodel import SQLModel

from icon_contracts.config import settings
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}".format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    server=settings.POSTGRES_SERVER,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DATABASE,
)

logger.info(f"Connecting to server: {settings.POSTGRES_SERVER} and {settings.POSTGRES_DATABASE}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Run onetime if we want to init with a prebuilt table of attributes
# async def init_db():
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         x = SQLModel.metadata
#         await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(init_db())
