import uuid

from pydantic import BaseModel

from screening_agent.ingestion.domain.enums import DocumentType


class DocumentResponse(BaseModel):
    id: uuid.UUID
    type: DocumentType
    filename: str
    content_hash: str

    class Config:
        from_attributes = True
