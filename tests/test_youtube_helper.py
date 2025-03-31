import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup, Tag
from youtube_transcript_api import YouTubeTranscriptApi
from parsethisio.content_parser.helpers.youtube_transcript_helper import YouTubeTranscriptHelper
from parsethisio.exceptions import RegexResultError, RemoteRequestError, NotFoundError

@pytest.fixture
def sample_urls():
    return {
        "valid": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "invalid": "https://youtube.com/invalid",
        "shorts": "https://youtube.com/shorts/dQw4w9WgXcQ",
        "embed": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    }

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_transcript_api():
    with patch('parsethisio.content_parser.helpers.youtube_transcript_helper.YouTubeTranscriptApi') as mock_api:
        mock_list = MagicMock()
        mock_api.list_transcripts = mock_list
        yield mock_api

def test_extract_video_id_valid(sample_urls):
    """Test that valid YouTube URL extracts correct video ID."""
    helper = YouTubeTranscriptHelper()
    video_id = helper.extract_video_id(sample_urls["valid"])
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_shorts(sample_urls):
    """Test that YouTube shorts URL extracts correct video ID."""
    helper = YouTubeTranscriptHelper()
    video_id = helper.extract_video_id(sample_urls["shorts"])
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_embed(sample_urls):
    """Test that YouTube embed URL extracts correct video ID."""
    helper = YouTubeTranscriptHelper()
    video_id = helper.extract_video_id(sample_urls["embed"])
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_invalid(sample_urls):
    """Test that invalid YouTube URL raises RegexResultError."""
    helper = YouTubeTranscriptHelper()
    with pytest.raises(RegexResultError):
        helper.extract_video_id(sample_urls["invalid"])

def test_get_video_title_success(mock_requests):
    """Test successful video title extraction."""
    mock_requests.return_value.text = '<meta property="og:title" content="Test Video">'
    helper = YouTubeTranscriptHelper()
    title = helper.get_video_title("dQw4w9WgXcQ")
    assert title == "Test Video"

def test_get_video_title_network_error(mock_requests):
    """Test network error handling in title extraction."""
    mock_requests.side_effect = Exception("Network error")
    helper = YouTubeTranscriptHelper()
    with pytest.raises(RemoteRequestError):
        helper.get_video_title("dQw4w9WgXcQ")

def test_get_video_title_missing_meta(mock_requests):
    """Test handling of missing meta tag in title extraction."""
    mock_requests.return_value.text = '<html><body>No meta tag</body></html>'
    helper = YouTubeTranscriptHelper()
    with pytest.raises(RemoteRequestError, match="Failed to fetch video title for dQw4w9WgXcQ"):
        helper.get_video_title("dQw4w9WgXcQ")

def test_get_best_transcript_manual(mock_transcript_api):
    """Test successful manual transcript retrieval."""
    mock_transcript = MagicMock()
    mock_transcript.is_generated = False
    mock_transcript.language_code = "en"
    mock_transcript.fetch.return_value = [{"text": "Test", "start": 0, "duration": 1}]
    
    mock_transcript_api.list_transcripts.return_value = [mock_transcript]
    
    helper = YouTubeTranscriptHelper()
    transcript = helper.get_best_transcript("dQw4w9WgXcQ")
    assert transcript == [{"text": "Test", "start": 0, "duration": 1}]

def test_get_best_transcript_auto_generated(mock_transcript_api):
    """Test auto-generated transcript fallback."""
    mock_transcript = MagicMock()
    mock_transcript.is_generated = True
    mock_transcript.language_code = "en"
    mock_transcript.fetch.return_value = [{"text": "Auto", "start": 0, "duration": 1}]
    
    mock_transcript_api.list_transcripts.return_value = [mock_transcript]
    
    helper = YouTubeTranscriptHelper()
    transcript = helper.get_best_transcript("dQw4w9WgXcQ")
    assert transcript == [{"text": "Auto", "start": 0, "duration": 1}]

def test_get_best_transcript_translation(mock_transcript_api):
    """Test translation fallback when no preferred language available."""
    mock_transcript = MagicMock()
    mock_transcript.is_translatable = True
    mock_transcript.translate.return_value.fetch.return_value = [{"text": "Translated", "start": 0, "duration": 1}]
    
    mock_transcript_api.list_transcripts.return_value = [mock_transcript]
    
    helper = YouTubeTranscriptHelper()
    transcript = helper.get_best_transcript("dQw4w9WgXcQ")
    assert transcript == [{"text": "Translated", "start": 0, "duration": 1}]

def test_get_best_transcript_not_found(mock_transcript_api):
    """Test error handling when no transcript is available."""
    mock_transcript_api.list_transcripts.return_value = []
    
    helper = YouTubeTranscriptHelper()
    with pytest.raises(RemoteRequestError, match="Failed to get transcript for video dQw4w9WgXcQ: No suitable transcript found"):
        helper.get_best_transcript("dQw4w9WgXcQ")

def test_clean_transcript_default_phrases():
    """Test removal of default phrases from transcript."""
    helper = YouTubeTranscriptHelper()
    transcript = [
        {"text": "[music] Hello", "start": 0, "duration": 1},
        {"text": "World [applause]", "start": 1, "duration": 1},
        {"text": "[laughter] Test", "start": 2, "duration": 1}
    ]
    cleaned = helper.clean_transcript(transcript)
    assert cleaned == "Hello World Test"

def test_clean_transcript_custom_phrases():
    """Test removal of custom phrases from transcript."""
    helper = YouTubeTranscriptHelper()
    transcript = [
        {"text": "[intro] Hello", "start": 0, "duration": 1},
        {"text": "World [outro]", "start": 1, "duration": 1}
    ]
    cleaned = helper.clean_transcript(transcript, remove_phrases=["[intro]", "[outro]"])
    assert cleaned == "Hello World"

def test_clean_transcript_invalid_entries():
    """Test handling of invalid transcript entries."""
    helper = YouTubeTranscriptHelper()
    transcript = [
        {"text": "Valid"},
        {"wrong_key": "Invalid"},
        {"text": 123},
        {"text": "Also Valid"}
    ]
    cleaned = helper.clean_transcript(transcript)
    assert cleaned == "Valid Also Valid"
