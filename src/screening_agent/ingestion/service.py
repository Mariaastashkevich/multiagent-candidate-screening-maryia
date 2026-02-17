import uuid

from sqlalchemy.orm import Session

from screening_agent.ingestion.domain.enums import DocumentType
from screening_agent.ingestion.exceptions import DocumentNotFoundError
from screening_agent.ingestion.models import DocumentsOrm
from screening_agent.ingestion.parsers.registry import ParserRegistry
from screening_agent.ingestion.repository import DocumentRepository
from screening_agent.ingestion.utils import calculate_content_hash


class IngestionService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = DocumentRepository(session)
        self.registry = ParserRegistry()

    def ingest(self, filename: str, file_bytes: bytes, doc_type: DocumentType):
        raw_text = self.registry.parse_bytes(filename, file_bytes)
        content_hash = calculate_content_hash(raw_text)

        existing = self.repo.get_by_hash(content_hash, doc_type)
        if existing:
            return existing

        document = self.repo.create(
            filename=filename,
            raw_text=raw_text,
            content_hash=content_hash,
            type=doc_type,
        )

        return document

    def reingest(self, filename: str, file_bytes: bytes, doc_id: uuid.UUID) -> DocumentsOrm:

        raw_text = self.registry.parse_bytes(filename, file_bytes)
        new_hash = calculate_content_hash(raw_text)

        document = self.repo.get(doc_id)
        if not document:
            raise DocumentNotFoundError("Document not found")

        if new_hash == document.content_hash:
            return document

        upd_document = self.repo.update(
            doc_id,
            raw_text=raw_text,
            content_hash=new_hash,
        )
        return upd_document


    def delete(self, doc_id: uuid.UUID):
        document = self.repo.get(doc_id)
        if not document:
            raise DocumentNotFoundError("Document not found")

        self.repo.delete(document)