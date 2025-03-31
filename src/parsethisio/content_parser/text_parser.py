from parsethisio.content_parser.base_parser import BaseParser
import json
from scrapegraphai.graphs import SmartScraperGraph
import re
import aiohttp
from bs4 import BeautifulSoup
from youtube_transcript_api.formatters import TextFormatter
from parsethisio.content_parser.helpers.youtube_transcript_helper import YouTubeTranscriptHelper
from gitingest import ingest
from parsethisio.utils import ResultFormat
from typing import Any

class TextParser(BaseParser):
    @property
    def supported_mimetypes(self) -> list:
        return [
            "text/plain"
        ]

    def parse(self, source: Any, result_format: ResultFormat = ResultFormat.TXT) -> str:
        """Parse content and return as string.
        
        Args:
            file_content: Content to parse (bytes or str)
            result_format: Desired output format
            
        Returns:
            str: Parsed content as string
            
        Raises:
            ValueError: If content type is not supported
        """
        if isinstance(source, bytes):
            return source.decode('utf-8')
        elif isinstance(source, str):
            if source.startswith("http"):
                if "youtube.com" in source:
                    return self.transcribe_youtube(source, result_format)
                elif "github.com" in source:
                    return self.scrape_github(source, result_format)
                return self.scrape_url(source, result_format)
            return source
        raise ValueError("Unsupported content type")
    
    def scrape_url(self, url: str, result_format: ResultFormat) -> str:
        """Scrape URL content and return as string.
        
        Args:
            url: URL to scrape
            result_format: Desired output format
            
        Returns:
            str: Scraped content as JSON string
        """
        graph_config = {
            "llm": {
                "api_key": "",
                "model": "openai/gpt-4o-mini",
            },
            "verbose": True,
            "headless": True,
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt="Give me all information from the website.",
            source=url,
            config=graph_config
        )

        result = smart_scraper_graph.run()
        return json.dumps(result, indent=4)
    
    def transcribe_youtube(self, url: str, result_format: ResultFormat) -> str:
        """Transcribe YouTube video and return as string.
        
        Args:
            url: YouTube video URL
            result_format: Desired output format
            
        Returns:
            str: Video title and transcript
            
        Raises:
            RegexResultError: If video ID cannot be extracted
            RemoteRequestError: If transcript/title cannot be fetched
        """
        helper = YouTubeTranscriptHelper()
        video_id = helper.extract_video_id(url)
        transcript = helper.get_best_transcript(video_id)
        title = helper.get_video_title(video_id)
        
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return f"{title}\n\n{formatted_transcript}"

    def scrape_github(self, url: str, result_format: ResultFormat) -> str:
        """Scrape GitHub repository content.
        
        Args:
            url: GitHub repository URL
            result_format: Desired output format
            
        Returns:
            str: Repository content
        """
        summary, tree, content = ingest(url)
        return content
