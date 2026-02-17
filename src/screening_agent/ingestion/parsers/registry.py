from pathlib import Path
from typing import Dict

from screening_agent.ingestion.exceptions import UnsupportedFileTypeError
from screening_agent.ingestion.parsers.base_parser import BaseParser
from screening_agent.ingestion.parsers.docx_parser import DocxParser
from screening_agent.ingestion.parsers.pdf_parser import PdfParser
from screening_agent.ingestion.parsers.txt_parser import TxtParser


class ParserRegistry:
    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {
            ".txt": TxtParser(),
            ".pdf": PdfParser(),
            ".docx": DocxParser(),
        }

    def get_parser(self, filename: Path | str) -> BaseParser:
        suffix = Path(filename).suffix.lower()
        try:
            return self._parsers[suffix]
        except KeyError:
            raise UnsupportedFileTypeError(f"Unsupported file type: {suffix}")

    def parse(self, path: Path) -> str:
        parser = self.get_parser(path)
        parsed = parser.parse(path)
        return parsed.raw_text

    def parse_bytes(self, filename: str, file_bytes: bytes) -> str:
        parser = self.get_parser(filename)
        parsed = parser.parse_bytes(filename, file_bytes)
        return parsed.raw_text

    def register(self, suffix: str, parser: BaseParser) -> None:
        self._parsers[suffix.lower()] = parser

