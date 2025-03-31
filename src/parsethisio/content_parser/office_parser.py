from parsethisio.content_parser.base_parser import BaseParser
from markitdown import MarkItDown
from io import BytesIO
from parsethisio.utils import ResultFormat
import tempfile
import filetype

class OfficeParser(BaseParser):
    def __init__(self):
        self.converter = MarkItDown()

    @property
    def supported_mimetypes(self) -> list:
        return [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # pptx
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx
            "application/vnd.ms-excel",  # xls
        ]

    def parse(self, file_content, result_format: ResultFormat) -> str:
        # Handle both bytes and file-like objects
        if hasattr(file_content, 'read'):
            content = file_content.read()
        else:
            content = file_content

        # Detect file extension based on mime type from magic/filetype
        extension = '.docx'  # default
        mime_type = filetype.guess(content).mime
        if 'presentation' in mime_type:
            extension = '.pptx'
        elif 'sheet' in mime_type or 'excel' in mime_type:
            extension = '.xlsx' if 'openxmlformats' in mime_type else '.xls'

        # MarkItDown expects a file path, so we need to write to a temp file
        with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            result = self.converter.convert(temp_file.name)
            text = result.text_content
            if result_format == ResultFormat.MD:
                # Convert first line to markdown header
                lines = text.split('\n')
                if lines:
                    lines[0] = f"# {lines[0]}"
                text = '\n'.join(lines)
            return text
