import pytest
from unittest.mock import patch, MagicMock
from parsethisio.content_parser.text_parser import TextParser
import json
from parsethisio import ResultFormat
from parsethisio.exceptions import RegexResultError, RemoteRequestError, NotFoundError

mocked_scraper_response = '''{"title": "Example Domain", "description": "This domain is for use in illustrative examples in documents.", "usage": "You may use this domain in literature without prior coordination or asking for permission.", "more_information_link": "https://www.iana.org/domains/example"}'''

@pytest.fixture
def mock_scrapegraph_ai():
    with patch('parsethisio.content_parser.text_parser.SmartScraperGraph') as MockSmartScraperGraph:
        mock_client = MockSmartScraperGraph.return_value
        mock_client.run.return_value = json.loads(mocked_scraper_response)
        yield mock_client

def test_text_parser(mock_scrapegraph_ai):
    parser = TextParser()

    text = parser.parse("http://jdde.de/", result_format=ResultFormat.TXT)
    
    parsedJsonText = json.loads(text)

    #dump and load again to have the same attribute order
    adjustedResponse = mocked_scraper_response
    adjustedText = json.dumps(parsedJsonText)

    assert adjustedText == adjustedResponse
    mock_scrapegraph_ai.run.assert_called_once()

mocked_youtube_transcribe_title = "Tagesschau"
mocked_youtube_transcribe_answer = [{'text': 'This is the First German Television\nwith the Tagesschau.', 'start': 4.28, 'duration': 3.68}, {'text': 'This broadcast was\nsubtitled live by NDR (22.12.2024)', 'start': 8.68, 'duration': 4.44}, {'text': 'Today in the studio:\nConstantin Schreiber.', 'start': 15.52, 'duration': 2.64}, {'text': 'Good evening to the Tagesschau.', 'start': 18.36, 'duration': 2.08}]
exptected_transcribe_as_string = '''
This is the First German Television
with the Tagesschau.
This broadcast was
subtitled live by NDR (22.12.2024)
Today in the studio:
Constantin Schreiber.
Good evening to the Tagesschau.'''
@pytest.fixture
def mock_youtube_transcript_logic():
    with patch('parsethisio.content_parser.text_parser.YouTubeTranscriptHelper') as MockYouTubeTranscriptHelper:
        mock_client = MockYouTubeTranscriptHelper.return_value
        mock_client.get_best_transcript.return_value = mocked_youtube_transcribe_answer
        mock_client.get_video_title.return_value = mocked_youtube_transcribe_title
        yield mock_client

def test_text_parser_youtube_url(mock_youtube_transcript_logic):
    parser = TextParser()

    text = parser.parse("https://www.youtube.com/watch?v=Cc_Su-YC_h4", result_format=ResultFormat.TXT)

    expectedOutcome = mocked_youtube_transcribe_title + "\n" + exptected_transcribe_as_string

    assert text == expectedOutcome
    mock_youtube_transcript_logic.get_best_transcript.assert_called_once()
    mock_youtube_transcript_logic.get_video_title.assert_called_once()



mocked_github_scrape_ingest_content = '''
================================================
File: /CODE_OF_CONDUCT.md
================================================
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.
'''
@pytest.fixture
def mock_gitingest_answer():
    with patch('parsethisio.content_parser.text_parser.ingest') as MockIngest:
        MockIngest.return_value = ('', '', mocked_github_scrape_ingest_content)

        yield MockIngest

def test_text_parser_github_url(mock_gitingest_answer):
    parser = TextParser()

    text = parser.parse("https://github.com/cyclotruc/gitingest", result_format=ResultFormat.TXT)

    assert text == mocked_github_scrape_ingest_content
    mock_gitingest_answer.assert_called_once()

def test_text_parser_invalid_input():
    """Test that parser raises ValueError for invalid input types."""
    parser = TextParser()
    
    with pytest.raises(ValueError, match="Unsupported content type"):
        parser.parse(123)  # Test non-bytes, non-string input
    
    with pytest.raises(ValueError, match="Unsupported content type"):
        parser.parse(["not", "valid"])  # Test list input
    
    with pytest.raises(ValueError, match="Unsupported content type"):
        parser.parse({"key": "value"})  # Test dict input

@pytest.fixture
def mock_scrapegraph_ai_error():
    """Mock SmartScraperGraph to simulate network errors."""
    with patch('parsethisio.content_parser.text_parser.SmartScraperGraph') as MockSmartScraperGraph:
        mock_client = MockSmartScraperGraph.return_value
        mock_client.run.side_effect = Exception("Network error")
        yield mock_client

def test_text_parser_scrape_url_error(mock_scrapegraph_ai_error):
    """Test that parser handles network errors during URL scraping."""
    parser = TextParser()
    with pytest.raises(Exception, match="Network error"):
        parser.parse("http://example.com", result_format=ResultFormat.TXT)

def test_text_parser_youtube_invalid_url(mock_youtube_transcript_logic):
    """Test that parser handles invalid YouTube URLs."""
    parser = TextParser()
    mock_youtube_transcript_logic.extract_video_id.side_effect = RegexResultError("Invalid URL")
    
    with pytest.raises(RegexResultError, match="Invalid URL"):
        parser.parse("https://youtube.com/invalid", result_format=ResultFormat.TXT)

def test_text_parser_youtube_no_transcript(mock_youtube_transcript_logic):
    """Test that parser handles missing YouTube transcripts."""
    parser = TextParser()
    mock_youtube_transcript_logic.extract_video_id.return_value = "valid_id"
    mock_youtube_transcript_logic.get_best_transcript.side_effect = NotFoundError("No transcript")
    
    with pytest.raises(NotFoundError, match="No transcript"):
        parser.parse("https://www.youtube.com/watch?v=valid_id", result_format=ResultFormat.TXT)

@pytest.fixture
def mock_gitingest_error():
    """Mock gitingest to simulate repository not found error."""
    with patch('parsethisio.content_parser.text_parser.ingest') as MockIngest:
        MockIngest.side_effect = Exception("Repository not found")
        yield MockIngest

def test_text_parser_github_error(mock_gitingest_error):
    """Test that parser handles GitHub repository not found error."""
    parser = TextParser()
    with pytest.raises(Exception, match="Repository not found"):
        parser.parse("https://github.com/invalid/repo", result_format=ResultFormat.TXT)
