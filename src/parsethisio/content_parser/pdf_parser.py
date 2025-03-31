from parsethisio.content_parser.base_parser import BaseParser
from PyPDF2 import PdfReader
from markitdown import MarkItDown
from io import BytesIO
from parsethisio.utils import ResultFormat
import tempfile

class PDFParser(BaseParser):
    def __init__(self):
        self.converter = MarkItDown()

    @property
    def supported_mimetypes(self) -> list:
        return [
            "application/pdf"
        ]

    def parse(self, file_content, result_format: ResultFormat) -> str:
        if result_format == ResultFormat.TXT:
            # Use PyPDF2 for backward compatibility
            if isinstance(file_content, bytes):
                file_content = BytesIO(file_content)
            reader = PdfReader(file_content)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
        else:
            # Use Markitdown for MD format
            if hasattr(file_content, 'read'):
                content = file_content.read()
            else:
                content = file_content
            with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
                temp_file.write(content)
                temp_file.flush()
                result = self.converter.convert(temp_file.name)
                return result.text_content
