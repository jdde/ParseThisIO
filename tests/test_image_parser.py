import pytest
from unittest.mock import patch, MagicMock
from parsethisio.content_parser.image_parser import ImageParser
from parsethisio import ResultFormat
# src/content_parser/test_image_parser.py
import os

image_test_file_path = 'tests/fixtures/test_data_diagram.png'
image_test_file_as_text = '''
```mermaid
graph LR
    xychart-beta
    title "Sales Revenue"
    x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    y-axis "Revenue (in $)" 4000 --> 11000
    bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
```
'''


@pytest.fixture
def mock_openai():
    with patch('parsethisio.content_parser.image_parser.OpenAI') as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=image_test_file_as_text))]
        )
        yield mock_client

def test_image_parser(mock_openai):
    parser = ImageParser()
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_diagram.png')
    
    with open(file_path, "rb") as f:
        result = parser.parse(f.read(), result_format=ResultFormat.TXT)

    assert result == image_test_file_as_text
    mock_openai.chat.completions.create.assert_called_once()