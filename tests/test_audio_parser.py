import pytest
from unittest.mock import patch, MagicMock
from parsethisio.content_parser.audio_parser import AudioParser
from parsethisio import ResultFormat
import os
# src/content_parser/test_audio_parser.py

audio_test_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_ttsmaker-test-generated-file.mp3')
audio_test_file_transkript = "Welcome to Eleven Degrees, your gateway to the cutting edge of innovation and the world of technology. I’m your host, Sam, and each week, we explore the latest trends, breakthroughs, and the people shaping the future of technology."

@pytest.fixture
def mock_openai():
    with patch('parsethisio.content_parser.audio_parser.OpenAI') as MockOpenAI:
        mock_client = MockOpenAI.return_value
        mock_client.audio.transcriptions.create.return_value = MagicMock(
            text=audio_test_file_transkript
        )
        yield mock_client

def test_audio_parser(mock_openai):
    parser = AudioParser()
    with open(audio_test_file_path, "rb") as f:
        result = parser.parse(f.read(), result_format=ResultFormat.TXT)

    assert result == audio_test_file_transkript
    mock_openai.audio.transcriptions.create.assert_called_once()

def test_audio_parser_markdown_result_equals_text_result(mock_openai):
    parser = AudioParser()
    with open(audio_test_file_path, "rb") as f:
        result = parser.parse(f.read(), result_format=ResultFormat.MD)

    assert result == audio_test_file_transkript
    mock_openai.audio.transcriptions.create.assert_called_once()

