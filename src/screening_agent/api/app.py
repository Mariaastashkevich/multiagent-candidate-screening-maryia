from fastapi import FastAPI
from screening_agent.api.routers.documents import router as documents_router


def create_app() -> FastAPI:
    app = FastAPI(title="Candidate Screening Helper")
    app.include_router(
        router=documents_router,
        prefix="/documents",
        tags=["documents"]
    )
    return app


