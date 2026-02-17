import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from screening_agent.infrastructure.db.base import Base
from screening_agent.ingestion.domain.enums import DocumentType


class DocumentsOrm(Base):
    __tablename__ = 'documents'

    __table_args__ = (
        UniqueConstraint('content_hash', "type", name='uq_doc_type_hash'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(nullable=False)
    raw_text: Mapped[str] = mapped_column(nullable=False)
    content_hash: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )