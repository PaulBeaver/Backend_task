from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.config import settings

# Metadata object for table definitions.
metadata = MetaData()

# Declarative base class for SQLAlchemy models.
Base = declarative_base(metadata=metadata)

# Create an asynchronous database engine with connection pooling.
engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=200,
    max_overflow=100,
    pool_timeout=300,
)

# Session factory for creating asynchronous database sessions.
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent objects from expiring after commit, useful for long-lived objects.
)
