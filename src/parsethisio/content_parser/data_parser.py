from parsethisio.content_parser.base_parser import BaseParser
from markitdown import MarkItDown
from io import BytesIO
from parsethisio.utils import ResultFormat
import tempfile

class DataParser(BaseParser):
    def __init__(self):
        self.converter = MarkItDown()

    @property
    def supported_mimetypes(self) -> list:
        return [
            "text/csv",  # CSV
            "application/json",  # JSON
            "application/xml",  # XML
            "text/xml",  # XML
        ]

    def parse(self, file_content, result_format: ResultFormat) -> str:
        # Handle both bytes and file-like objects
        if hasattr(file_content, 'read'):
            content = file_content.read()
        else:
            content = file_content

        # Use file extension directly since these are text-based formats
        if b'<?xml' in content[:10] or b'<rss' in content[:10]:
            extension = '.xml'
        elif b'{' in content[:10]:
            extension = '.json'
        else:
            extension = '.csv'

        # MarkItDown expects a file path, so we need to write to a temp file
        with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            result = self.converter.convert(temp_file.name)
            text = result.text_content
            if result_format == ResultFormat.MD:
                if extension == '.json':
                    text = f"```json\n{text}\n```"
                elif extension == '.xml':
                    text = f"```xml\n{text}\n```"
            return text
