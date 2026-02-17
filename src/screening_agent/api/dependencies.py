from typing import Generator

from sqlalchemy.orm import Session

from screening_agent.infrastructure.db.session import get_session_factory


def get_db_session() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()