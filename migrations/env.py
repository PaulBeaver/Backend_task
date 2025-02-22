import asyncio
from logging.config import fileConfig
import os

if os.environ.get("PYTEST"):
    import pytest

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings
from app.models import Base

# Retrieve the Alembic Config object, which provides access to the .ini file.
config = context.config

# Set database connection options dynamically from environment variables.
section = config.config_ini_section
config.set_section_option(section, "DB_HOST", settings.DB_HOST)
config.set_section_option(section, "DB_NAME", settings.DB_NAME)
config.set_section_option(section, "DB_PASS", settings.DB_PASS)
config.set_section_option(section, "DB_PORT", settings.DB_PORT)
config.set_section_option(section, "DB_USER", settings.DB_USER)

# Configure logging based on the Alembic configuration file.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support.
target_metadata = [Base.metadata]


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and does not require a database connection.
    Calls to `context.execute()` will output SQL statements to the console or migration file.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Execute migrations in an active database connection.

    Args:
        connection (Connection): Database connection provided by SQLAlchemy.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run asynchronous migrations in 'online' mode.

    This method creates an async engine and binds a connection to the Alembic context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    This method runs asynchronous migrations using `asyncio.run()`.
    """
    asyncio.run(run_async_migrations())


# Determine whether to run offline or online migrations based on the context.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
