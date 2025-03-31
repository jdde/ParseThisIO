import unittest
from unittest.mock import patch, MagicMock
import parsethisio
from parsethisio.content_parser.pdf_parser import PDFParser
from parsethisio import ResultFormat
import os
class TestAutomaticParsing(unittest.TestCase):
    def test_get_pdf_parser(self):
        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'text_data_meeting_notes.pdf')
    
        with open(file_path, "rb") as f:
            result = parsethisio.parse(f.read(), result_format=ResultFormat.TXT)

            pypddf2ExpectedText= """YOUR
COMPANY 
MEETING
NAME
09/04
04
SEPTEMBER
20XX
/
4:30
PM
/
ROOM
436
ATTENDEES
Wendy
Writer,
Ronny
Reader,
Abby
Author
AGENDA
Last
Meeting
Follow-up
1.
Lorem
ipsum
dolor
sit
amet,
consectetuer
adipiscing
elit.
New
Business
●
Lorem
ipsum
dolor
sit
amet,
consectetuer
adipiscing
elit.
●
Suspendisse
scelerisque
mi
a
mi.
NOTES
●
Lorem
ipsum
dolor
sit
amet
consectetuer
adipiscing
elit.
●
Vestibulum
ante
ipsum
primis
elementum
,
libero
interdum
auctor
cursus,
sapien
enim
dictum
quam.
○
Phasellus
vehicula
nonummy
ACTION
ITEMS
1.
Lorem
ipsum
dolor
sit
amet
consectetuer
adipiscing
elit.
NEXT
W EEK’S
AGENDA
Lorem
ipsum
dolor
sit
amet,
consectetuer
adipiscing
elit.
"""

            assert result == pypddf2ExpectedText


if __name__ == '__main__':
    unittest.main()