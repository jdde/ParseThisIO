import re
import requests
from bs4 import BeautifulSoup, Tag
from youtube_transcript_api import YouTubeTranscriptApi
from loguru import logger
from parsethisio.exceptions import RegexResultError, RemoteRequestError, NotFoundError

class YouTubeTranscriptHelper:
    """Helper class to manage YouTube transcript extraction and metadata retrieval."""

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extracts the YouTube video ID from various URL formats.

        Args:
            url: The YouTube video URL

        Returns:
            str: The YouTube video ID

        Raises:
            RegexResultError: When regex wasnt able to find videoId
        """
        youtube_regex = (
            r"(?:https?://)?(?:www\.)?"
            r"(?:youtu\.be/|youtube\.com(?:/embed/|/v/|/watch\?v=|/watch\?.+&v=|/shorts/))"
            r"([\w-]{11})"
        )
        match = re.search(youtube_regex, url)
        if not match:
            raise RegexResultError(f"Failed to extract video ID from {url}")

        return match.group(1)

    @staticmethod
    def get_video_title(video_id: str) -> str:
        """
        Fetches the title of the YouTube video using the video ID.

        Args:
            video_id: The YouTube video ID

        Returns:
            str: The video title

        Raises:
            RemoteRequestError: When we were not able to fetch the youtube url
            RegexResultError: When we cant parse the title from the html
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = requests.get(url)
            html = response.text

            soup = BeautifulSoup(html, "html.parser")
            meta = soup.find("meta", property="og:title")
            if not meta or not isinstance(meta, Tag) or not meta.get("content"):
                raise RegexResultError(f"Failed to extract video title from {url}")
            
            content = meta.get("content")
            if not isinstance(content, str):
                raise RegexResultError(f"Invalid title content type from {url}")
            
            return content
        except Exception as e:
            raise RemoteRequestError(f"Failed to fetch video title for {video_id}: {e}")

    #TODO: update preferred langs?
    @staticmethod
    def get_best_transcript(video_id: str, preferred_langs: list[str] = ["en", "es", "pt"]) -> list[dict[str, str | float]]:
        """
        Retrieves the best transcript for a YouTube video.

        Args:
            video_id: The YouTube video ID
            preferred_langs: Preferred languages for the transcript

        Returns:
            list[dict[str, str | float]]: The transcript entries with text and timing info

        Raises:
            NotFoundError: When no suitable transcript is found
            RemoteRequestError: When we were not able to fetch the youtube url
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Prioritize manual transcripts
            for lang in preferred_langs:
                for transcript in transcript_list:
                    if not transcript.is_generated and transcript.language_code == lang:
                        return transcript.fetch()

            # Fallback to auto-generated transcripts
            for lang in preferred_langs:
                for transcript in transcript_list:
                    if transcript.is_generated and transcript.language_code == lang:
                        return transcript.fetch()

            # Fallback to translated transcripts
            for transcript in transcript_list:
                if transcript.is_translatable:
                    translation = transcript.translate(preferred_langs[0])
                    return translation.fetch()

            raise NotFoundError("No suitable transcript found")
        except Exception as e:
            raise RemoteRequestError(f"Failed to get transcript for video {video_id}: {e}")

    @staticmethod
    def clean_transcript(transcript: list[dict[str, str | float]], remove_phrases: list[str] | None = None) -> str:
        """
        Cleans the transcript by removing unwanted phrases or tags.

        Args:
            transcript: The raw transcript entries with text and timing info
            remove_phrases: A list of phrases to remove (case-insensitive)

        Returns:
            str: The cleaned transcript as a single string
        """
        if not remove_phrases:
            remove_phrases = ["[music]", "[applause]", "[laughter]"]

        cleaned_texts: list[str] = []
        for entry in transcript:
            text = entry.get("text")
            if not isinstance(text, str):
                continue
            
            cleaned_text = text
            for phrase in remove_phrases:
                cleaned_text = cleaned_text.replace(phrase, "").strip()
            
            if cleaned_text:
                cleaned_texts.append(cleaned_text)

        return " ".join(cleaned_texts)
