import unittest
from unittest.mock import patch, MagicMock
import parsethisio
from parsethisio.content_parser.audio_parser import AudioParser
from parsethisio.content_parser.image_parser import ImageParser
from parsethisio.content_parser.pdf_parser import PDFParser
from parsethisio.content_parser.text_parser import TextParser
from io import BytesIO
import os

class TestAutomaticParserSelection(unittest.TestCase):
    def test_get_image_parser(self):
        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_diagram.png')
    
        with open(file_path, "rb") as f:
            # Call the function
            parser = parsethisio.get_parser(f.read())

            #assert parser is of class ImageParser
            assert isinstance(parser, ImageParser)

    def test_get_pdf_parser(self):
        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'text_data_meeting_notes.pdf')
    
        with open(file_path, "rb") as f:
            # Call the function
            parser = parsethisio.get_parser(f.read())

            #assert parser is of class ImageParser
            assert isinstance(parser, PDFParser)

    def test_get_audio_parser(self):
        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_data_ttsmaker-test-generated-file.mp3')
    
        with open(file_path, "rb") as f:
            # Call the function
            parser = parsethisio.get_parser(f.read())

            #assert parser is of class ImageParser
            assert isinstance(parser, AudioParser)

    def test_get_text_parser_by_url(self):
        # Call the function
        parser = parsethisio.get_parser("http://jdde.de", mime_type="text/plain")

        #assert parser is of class ImageParser
        assert isinstance(parser, TextParser)

    def test_get_text_parser_by_url(self):
        # Call the function
        parser = parsethisio.get_parser("This is a normal, awesome text", mime_type="text/plain")

        #assert parser is of class ImageParser
        assert isinstance(parser, TextParser)


if __name__ == '__main__':
    unittest.main()