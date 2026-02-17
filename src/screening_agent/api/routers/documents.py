import uuid

from fastapi import Depends, APIRouter, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from screening_agent.api.dependencies import get_db_session
from screening_agent.api.schemas.document import DocumentResponse
from screening_agent.ingestion.domain.enums import DocumentType
from screening_agent.ingestion.exceptions import UnsupportedFileTypeError, DocumentNotFoundError
from screening_agent.ingestion.service import IngestionService

router = APIRouter()


@router.post(
    "/ingest",
    response_model=DocumentResponse,
    status_code=201
)
async def ingest_document(
        file: UploadFile = File(...),
        doc_type: DocumentType = Form(...),
        session: Session = Depends(get_db_session)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty")

    service = IngestionService(
        session=session
    )

    try:
        result = service.ingest(
            filename=file.filename,
            file_bytes=file_bytes,
            doc_type=doc_type
        )
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.post(
    "/{doc_id}/reingest",
    response_model=DocumentResponse,
    status_code=201
)
async def reingest_document(
        doc_id: uuid.UUID,
        file: UploadFile = File(...),
        session: Session = Depends(get_db_session)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty")

    service = IngestionService(
        session=session
    )

    try:
        result = service.reingest(
            filename=file.filename,
            file_bytes=file_bytes,
            doc_id=doc_id,
        )
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result


@router.delete(
    "/{doc_id}",
    status_code=204
)
async def delete_document(
        doc_id: uuid.UUID,
        session: Session = Depends(get_db_session)
):
    service = IngestionService(
        session=session
    )
    try:
        service.delete(doc_id=doc_id)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

