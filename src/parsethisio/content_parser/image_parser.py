from parsethisio.content_parser.base_parser import BaseParser
from typing import BinaryIO
from openai import OpenAI
import base64
from parsethisio.utils import ResultFormat
from loguru import logger
from parsethisio.exceptions import ParsingFailed
'''
Approach: Send image to openAI, get markdown/text back - return it
'''
class ImageParser(BaseParser):
    @property
    def supported_mimetypes(self) -> list:
        return [
            "image/jpeg",
            "image/png"
        ]

    def parse(self, file_obj: BinaryIO, result_format: ResultFormat) -> str:
        client = OpenAI()

        #image file_content as base64 string:
        base64_image = base64.b64encode(file_obj).decode('utf-8')

        prompt_result_hint = ""
        if result_format == ResultFormat.MD:
            prompt_result_hint = "Answer in markdown format."
        elif result_format == ResultFormat.TXT:
            prompt_result_hint = "Answer in text format."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "What is in this image? When the image contains a Diagram, give me the diagram as mermaid code. Give me the mermaid code only then, without any description. " + prompt_result_hint,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                    },
                    },
                ],
                }
            ],
        )

        if len(response.choices) == 0:
            logger.error("No response from openai")

            raise ParsingFailed("Image parsing failed")
        else:
            logger.debug(response.choices[0])

            return response.choices[0].message.content
        