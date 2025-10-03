from loguru import logger
import sys
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

from icon_contracts.config import settings

SQLALCHEMY_DATABASE_URL_STUB = "://{user}:{password}@{server}:{port}/{db}".format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    server=settings.POSTGRES_SERVER,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DATABASE,
)

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2" + SQLALCHEMY_DATABASE_URL_STUB

logger.info(
    f"Connecting worker to server: {settings.POSTGRES_SERVER} and {settings.POSTGRES_DATABASE}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_factory = sessionmaker(bind=engine)

def get_db_session():
    try:
        session = session_factory()
        return session
    except OperationalError as e:
        logger.error(f"Error connecting to the database: {e}")
        sys.exit(1)

# Use the function to get a session
session = get_db_session()
