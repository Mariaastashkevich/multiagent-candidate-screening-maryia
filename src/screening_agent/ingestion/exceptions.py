from screening_agent.core.exceptions import ScreeningAgentError


class IngestionError(ScreeningAgentError):
    """Base exception for ingestion module."""
    pass


class DocumentNotFoundError(IngestionError):
    """Raised when a document could not be found."""
    pass


class InvalidUpdateFieldError(IngestionError):
    """Raised when trying to update forbidden field."""
    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when a file type is not supported."""
    pass


