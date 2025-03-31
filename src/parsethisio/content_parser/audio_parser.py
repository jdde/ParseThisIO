from parsethisio.content_parser.base_parser import BaseParser
from typing import BinaryIO
from PyPDF2 import PdfReader
import io
from openai import OpenAI
import base64
from parsethisio.utils import ResultFormat

class AudioParser(BaseParser):
    @property
    def supported_mimetypes(self) -> list:
        return [
            "audio/ogg",
            "audio/mpeg",
            "audio/mp3",
            "audio/mp4",
            "audio/mpga",
            "audio/m4a",
            "audio/wav",
            "audio/webm",
        ]

    def parse(self, file_content: BinaryIO, result_format: ResultFormat) -> str:
        client = OpenAI()

        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')
        tmp_file_content = io.BytesIO(file_content)

        #TOOD: remove hardcoded "audio/mpeg" definition
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=("test.mp3", tmp_file_content, "audio/mpeg")
        )

        #for this parser, text and markdown result is equal
        return transcription.text