import uuid
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select

from screening_agent.ingestion.domain.enums import DocumentType
from screening_agent.ingestion.exceptions import DocumentNotFoundError, InvalidUpdateFieldError
from screening_agent.ingestion.models import DocumentsOrm

ALLOWED_UPDATE_FIELDS = {"raw_text", "filename", "content_hash", "type"}


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **fields) -> DocumentsOrm:
        document = DocumentsOrm(**fields)
        self.session.add(document)
        self.session.flush()
        return document

    def get(self, doc_id: uuid.UUID) -> DocumentsOrm | None:
        return self.session.get(DocumentsOrm, doc_id)

    def get_by_hash(self, content_hash: str, doc_type: DocumentType) -> DocumentsOrm | None:
        stmt = select(DocumentsOrm).where(
            DocumentsOrm.type == doc_type,
            DocumentsOrm.content_hash == content_hash
        )
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def delete(self, document: DocumentsOrm) -> None:
        self.session.delete(document)

    def update(self, doc_id: uuid.UUID, **fields: Any) -> DocumentsOrm:
        document = self.get(doc_id)
        if not document:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        for field, value in fields.items():
            if field not in ALLOWED_UPDATE_FIELDS:
                raise InvalidUpdateFieldError(f"Invalid field: {field}")
            setattr(document, field, value)

        return document






