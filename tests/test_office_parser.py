import os
from parsethisio.content_parser.office_parser import OfficeParser
from parsethisio.utils import ResultFormat
import filetype

def test_docx_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_sample.docx')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = filetype.guess(content).mime
        assert mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        parser = OfficeParser()
        # Test TXT format
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "AutoGen: Enabling Next-Gen LLM Applications" in text

        # Test MD format
        md_text = parser.parse(content, result_format=ResultFormat.MD)
        assert isinstance(md_text, str)
        assert len(md_text) > 0
        assert "# AutoGen: Enabling Next-Gen LLM Applications" in md_text

def test_pptx_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_presentation.pptx')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = filetype.guess(content).mime
        assert mime == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        
        parser = OfficeParser()
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "AutoGen: Enabling Next-Gen LLM Applications" in text

def test_xlsx_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_spreadsheet.xlsx')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = filetype.guess(content).mime
        assert mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        parser = OfficeParser()
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "Sheet1" in text

def test_xls_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_spreadsheet.xls')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = filetype.guess(content).mime
        assert mime == "application/vnd.ms-excel"
        
        parser = OfficeParser()
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "Sheet1" in text
