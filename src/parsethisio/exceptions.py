from loguru import logger

class ParseThisError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        logger.error(message)
        logger.exception(message)
        super().__init__(message)

class ParserNotFoundError(ParseThisError):
    """Exception raised when the magic parser detection wasnt able to find a parser."""
    pass

class UnsupportedMimeTypeError(ParseThisError):
    """Exception raised when the mime type is not supported by any parser."""
    pass

class RegexResultError(ParseThisError):
    """Exception raised when the regex search result is None."""
    pass

class RemoteRequestError(ParseThisError):
    """Exception raised for failing requests during parsing."""
    pass

class NotFoundError(ParseThisError):
    """Exception raised when the requested resource was not found."""
    pass

class ParsingFailed(ParseThisError):
    """Exception raised when parsing fails."""
    pass