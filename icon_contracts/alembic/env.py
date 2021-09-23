# from icon_contracts.models.alembic_base import Base

# from sqlalchemy import engine_from_config, pool

from icon_contracts.models import *

import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from alembic import context

from icon_contracts.db import ASYNC_SQLALCHEMY_DATABASE_URL

# TODO: Make sure this works!!!
# Other versions imported each object
from icon_contracts import models

config = context.config

config.set_main_option('sqlalchemy.url', ASYNC_SQLALCHEMY_DATABASE_URL)

fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    url = ASYNC_SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    x = config.get_section(config.config_ini_section)
    print()

    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# def run_migrations_online():
#     configuration = config.get_section(config.config_ini_section)
#     configuration["sqlalchemy.url"] = SQLALCHEMY_DATABASE_URL
#     connectable = engine_from_config(
#         configuration,
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#
#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata, compare_type=True
#         )
#
#         with context.begin_transaction():
#             context.run_migrations()

# if context.is_offline_mode():
#
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())
#     # run_migrations_online()
asyncio.run(run_migrations_online())


