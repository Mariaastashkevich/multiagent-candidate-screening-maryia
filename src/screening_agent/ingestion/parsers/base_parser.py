from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class ParsedDocument:
    raw_text: str
    filename: str


class BaseParser(Protocol):
    def parse(self, path: Path) -> ParsedDocument: ...
    def parse_bytes(self, filename: str, file_bytes: bytes) -> ParsedDocument: ...