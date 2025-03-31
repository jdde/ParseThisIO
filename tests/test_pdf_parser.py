import pytest
from parsethisio.content_parser.pdf_parser import PDFParser
from parsethisio.parsethisio import ResultFormat
import os

def test_pdf_parser():
    file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'text_data_meeting_notes.pdf')
    
    with open(file_path, "rb") as f:
        parser = PDFParser()
        text = parser.parse(f, result_format=ResultFormat.TXT)
        
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

    assert text == pypddf2ExpectedText
