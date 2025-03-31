import os
import mimetypes
from parsethisio.content_parser.data_parser import DataParser
from parsethisio.utils import ResultFormat

def test_csv_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_table.csv')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = mimetypes.guess_type(file_path)[0]
        assert mime == "text/csv"
        
        parser = DataParser()
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "名前,年齢,住所" in text  # Check CSV header (Japanese)

def test_json_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_config.json')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = mimetypes.guess_type(file_path)[0]
        assert mime == "application/json"
        
        parser = DataParser()
        # Test TXT format
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert '"key1": "string_value"' in text

        # Test MD format
        md_text = parser.parse(content, result_format=ResultFormat.MD)
        assert isinstance(md_text, str)
        assert len(md_text) > 0
        assert "```json" in md_text

def test_xml_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_feed.xml')
    
    with open(file_path, "rb") as f:
        content = f.read()
        mime = mimetypes.guess_type(file_path)[0]
        assert mime == "application/xml"
        
        parser = DataParser()
        text = parser.parse(content, result_format=ResultFormat.TXT)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "The Official Microsoft Blog" in text
