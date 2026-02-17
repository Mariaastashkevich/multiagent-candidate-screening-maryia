from pathlib import Path

from screening_agent.ingestion.parsers.base_parser import BaseParser


class TxtParser(BaseParser):
    def parse(self, path: Path):
        pass
