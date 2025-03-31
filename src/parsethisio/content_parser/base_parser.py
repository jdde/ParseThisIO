from abc import ABC, abstractmethod
from parsethisio.utils import ResultFormat
class BaseParser(ABC):
    @abstractmethod
    def parse(self, source, result_format: ResultFormat = ResultFormat.TXT) -> str:
        """Parse text from the given source."""
        pass

    @property
    @abstractmethod
    def supported_mimetypes(self) -> list:
        """List of supported MIME types."""
        pass
