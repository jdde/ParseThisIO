import os
from parsethisio.content_parser.archive_parser import ArchiveParser
from parsethisio.utils import ResultFormat
import filetype

def test_archive_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_archive.zip')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = filetype.guess(content).mime
        assert mime == "application/zip"
        
        parser = ArchiveParser()
        # Test TXT format
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Test MD format
        md_text = parser.parse(content, result_format=ResultFormat.MD)
        assert isinstance(md_text, str)
        assert len(md_text) > 0
        assert "# Archive Contents" in md_text
