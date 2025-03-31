from .base_parser import BaseParser
from markitdown import MarkItDown
from io import BytesIO
from parsethisio.utils import ResultFormat
import tempfile

class ArchiveParser(BaseParser):
    def __init__(self):
        self.converter = MarkItDown()

    @property
    def supported_mimetypes(self) -> list:
        return [
            "application/zip",  # ZIP
            "application/x-zip-compressed",  # ZIP
        ]

    def parse(self, file_content, result_format: ResultFormat) -> str:
        # Handle both bytes and file-like objects
        if hasattr(file_content, 'read'):
            content = file_content.read()
        else:
            content = file_content

        # MarkItDown expects a file path, so we need to write to a temp file
        with tempfile.NamedTemporaryFile(suffix='.zip') as temp_file:
            temp_file.write(content)
            temp_file.flush()
            result = self.converter.convert(temp_file.name)
            text = result.text_content
            if result_format == ResultFormat.MD:
                text = f"# Archive Contents\n\n{text}"
            return text
