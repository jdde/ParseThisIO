import mimetypes
import filetype

#available parsers
from parsethisio.content_parser.audio_parser import AudioParser
from parsethisio.content_parser.image_parser import ImageParser
from parsethisio.content_parser.pdf_parser import PDFParser
from parsethisio.content_parser.text_parser import TextParser
from parsethisio.content_parser.office_parser import OfficeParser
from parsethisio.content_parser.data_parser import DataParser
from parsethisio.content_parser.archive_parser import ArchiveParser

from parsethisio.exceptions import ParserNotFoundError, UnsupportedMimeTypeError
from parsethisio.utils import ResultFormat
PARSERS = [
    AudioParser,
    ImageParser,
    PDFParser,
    TextParser,
    OfficeParser,
    DataParser,
    ArchiveParser,
]

def parse(binary_file_data: bytes, file_name: str = None, mime_type: str = None, result_format: ResultFormat = ResultFormat.TXT):
    """
    Parse the given input source.

    This function takes an input source and performs parsing operations.
    When you dont provide file_name and mime_type, it will try to identify the file type automatically.
    When you encounter problems with automatic identification, you can provide file_name and mime_type manually.

    Args:
        binary_file_data (str): The source to be parsed.
        file_name (str): The filename will help to identify file type automatically.
        mime_type (str): The mime type will help to identify file type automatically

    Returns:
        str || None: The parsed content.

    Raises:
        ParserNotFoundError: If no parser is found for the given input.
        UnsupportedMimeTypeError: If the MIME type is unsupported.
        ParseThisError: For parsethis specific errors from sublogics
    """

    parser = get_parser(binary_file_data, file_name, mime_type)

    return parser.parse(binary_file_data, result_format)

def get_parser(binary_file_data: bytes, file_name: str = None, mime_type: str = None):
    """
    Determines the appropriate parser for the given input source.

    This function attempts to identify the appropriate parser based on the provided MIME type,
    file name, or the content of the binary file data. It prioritizes the MIME type if provided,
    followed by the file name, and finally attempts to guess the type based on the file content.

    Args:
        binary_file_data (bytes): The binary data of the file to be parsed.
        file_name (str, optional): The name of the file, used to help identify the file type.
        mime_type (str, optional): The MIME type of the file, used to identify the file type.

    Returns:
        Parser: The parser object that can handle the given input.

    Raises:
        ParserNotFoundError: If no parser is found for the given input.
        UnsupportedMimeTypeError: If the MIME type is unsupported.
    """
    #mime_type is most specific, lets use it if it's provided
    if mime_type is not None:
        return get_parser_by_mime_type(mime_type)
    
    #file_name is less specific, lets use it if it's provided
    if file_name is not None:
        mime_type = mimetypes.guess_type(file_name)[0]
        return get_parser_by_mime_type(mime_type)

    #if we dont have any information, lets try to guess the type based on file content
    kind = filetype.guess(binary_file_data)
    if kind is not None:
        return get_parser_by_mime_type(kind.mime)

    raise ParserNotFoundError("No parser found for the given input")

def get_parser_by_mime_type(mime_type: str):
    """
    Reads all Parser in content_parser folder, loads available mime_types and 
    returns the matching parser for the given mime_type.

    Args:
        mime_type (str): The MIME type to find a parser for.

    Returns:
        Parser: The parser object that can handle the given MIME type.

    Raises:
        UnsupportedMimeTypeError: If no parser supports the given MIME type.
    """

    for parser in PARSERS:
        parserObj = parser()
        if mime_type in parserObj.supported_mimetypes:
            return parserObj

    raise UnsupportedMimeTypeError("Unsupported MIME type: {mime_type}")

def get_supported_extensions() -> list[str]:
    """
    Get a list of all file extensions supported by any parser.
    
    Returns:
        list[str]: List of supported file extensions including the dot (e.g. ['.pdf', '.jpg'])
    """
    extensions = set()
    for parser in PARSERS:
        parser_obj = parser()
        for mime_type in parser_obj.supported_mimetypes:
            # Get all extensions for this mime type
            if mime_type:  # Skip None values
                exts = mimetypes.guess_all_extensions(mime_type)
                if exts:  # Skip empty lists
                    extensions.update(exts)
    return sorted(list(extensions))

# Pre-compute the list of extensions
supported_extensions = get_supported_extensions()

