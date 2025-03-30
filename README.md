# ParseThisIO

![Coverage](./coverage.svg)
![PyPI](https://img.shields.io/pypi/v/ParseThis)
![Build Status](https://img.shields.io/github/workflow/status/jdde/ParseThis/CI)
![License](https://img.shields.io/github/license/jdde/ParseThis)


**ParseThisIO** is a powerful and flexible tool with zero additional OS dependencies that makes raw data effortlessly readable and structured for your AI and data processing workflows. Whether you're extracting information from PDFs, transforming files into Markdown, or preparing data for LLMs and RAG pipelines, **ParseThisIO** gets the job done—quickly, effectively, and with a touch of magic.
Just install as a pip package and enjoy, no configuring around with third-party tools before you can use this package. Just parseThis.io.

For some parsers, there are API keys required. They're not required when you just don't use them—they will error on usage when no API key was found.

ParseThis aggregates multiple open-source projects to avoid re-implementing a file type mapping for content conversion.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [ParserMatrix - Dependency overview](#ParserMatrix)
- [Testing](#Testing)
- [License](#License)

---

## Features
- Auto-detects file types (pdf, docx, csv, pptx, xlsx, xls, json, xml, zip, mp3, mp4 and more).
- Converts any file into readable Markdown or plain text.
- Extracts structured data for use in LLM and RAG pipelines.
- Simple API for seamless integration into your workflows.
- Just forward user input to ParseThis and get Text || markdown.

The mapping of parser to file type can be found in the [ParserMatrix](#parsermatrix---when-is-which-dependency-used).

```python
import parsethisio

#get list of supported file extensions via 
parsethisio.get_supported_extensions()
```


---

## Prerequisites
Use Python 3.12 - maximum version supported by PyO3 - dependency of scrapegraph-ai, use a virtual environment with version 3.12
```sh
python3.12 -m venv myenv
source myenv/bin/activate
```

---

## Installation

To install **ParseThisIO**, use pip:

```bash
pip install parsethisio
```

---

## Usage
Use the parse() function to auto-detect the current type of content - when the autodetection is not working you can provide more information to help detect the type.
The auto-parse function accepts any input - file_path, url strings, file byte content.
```python
import parsethisio

#extract image description for llm
with open('tests/fixtures/test_data_diagram.png', 'rb') as f:
    image_description = parsethisio.parse(f.read(), result_format=ResultFormat.TXT)

#get transcript of audio
with open('tests/fixtures/test_data_ttsmaker-test-generated-file.mp3', 'rb') as f:
    audio_transcript = parsethisio.parse(f.read(), result_format=ResultFormat.TXT)
```

The generic parse() function detects automatically which parsers will be used based on the file content.

```python
import parsethisio

from parsethisio import ResultFormat


#automatic parse based on file_path
parsed_pdf_text = parsethisio.parse('tests/fixtures/text_data_meeting_notes.pdf', result_format=ResultFormat.TXT)

#automatic parse based on file content
with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    parsed_pdf_text = parsethisio.parse(f.read(), result_format=ResultFormat.TXT)  # works with any bytes content

#automatic parse based on string
parsed_github_repository = parsethisio.parse('https://github.com/jdde/ParseThis', result_format=ResultFormat.TXT)

#automatic parse based on YouTube URL
transcribed_youtube_text = parsethisio.parse('https://www.youtube.com/watch?v=ca7QkcAGe', result_format=ResultFormat.TXT)
```

Use the parser detection when you want to just find the parser and configure it differently before it parses the content.
```python
import parsethisio

with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    file_content = f.read()
    parser = parsethisio.get_parser(file_content)
    text = parser.parse(file_content)
```

Or just directly use a parser.
```python
from parsethisio import PDFParser

with open('tests/fixtures/text_data_meeting_notes.pdf', 'rb') as f:
    text = PDFParser.parse(file_content)
```

For more examples how to use it - see our [testing section](tests/test_automatic_parser_selection.py).

---

## ParserMatrix
Overview of dependencies used for specific parsing processes.

| File Type | Parser         | Dependency          | External Access Required |
|-----------|----------------|---------------------|---------------------|
| PDF       | PDFParser      | PyPDF2, Markitdown | ❌ |
| Image     | ImageParser    | OpenAI GPT         | ✅ env.OPENAI_API_KEY|
| Audio     | AudioParser    | OpenAI Whisper     | ✅ env.OPENAI_API_KEY |
| URL       | TextParser     | scrapegraphai      | ✅ env.OPENAI_API_KEY |
| YouTube   | TextParser  | youtube-transcript-api | ❌ |
| Github    | TextParser     | gitingest          | ❌ |
| DOCX      | OfficeParser   | Markitdown         | ❌ |
| PPTX      | OfficeParser   | Markitdown         | ❌ |
| XLSX/XLS  | OfficeParser   | Markitdown         | ❌ |
| CSV       | DataParser     | Markitdown         | ❌ |
| JSON      | DataParser     | Markitdown         | ❌ |
| XML       | DataParser     | Markitdown         | ❌ |
| ZIP       | ArchiveParser  | Markitdown         | ❌ |


If you're working with the source code, you can install all dependencies using:

```bash
pip install .
```
For more information, see the [how we install it in our github action](.github/workflows/coverage.yml).


## Testing
To execute tests use this:

```bash
coverage run -m pytest
#or for a single test:
pytest -k test_text_parser_github_url
```


## License
This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
