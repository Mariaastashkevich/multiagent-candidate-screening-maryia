from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from screening_agent.config.settings import get_settings


@lru_cache
def get_sync_engine():
    settings = get_settings()
    return create_engine(
        url=settings.DB_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
    )


@lru_cache
def get_session_factory():
    return sessionmaker(
        bind=get_sync_engine(),
        autocommit=False,
        autoflush=False,
    )



