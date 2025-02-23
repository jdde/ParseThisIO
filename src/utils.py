import base64
from enum import Enum
from urllib.parse import urlparse
import os


class ResultFormat(Enum):
    MD = "markdown"
    TXT = "txt"


def _is_url(source) -> bool:
    if not isinstance(source, str):
        return False
    parsed = urlparse(source)
    return parsed.scheme in ["http", "https"]

def _is_file_path(source) -> bool:
    return isinstance(source, str) and os.path.exists(source)

def _is_stream(source) -> bool:
    return hasattr(source, "read")

def _is_base64(source) -> bool:
    if not isinstance(source, str):
        return False
    try:
        base64.b64decode(source, validate=True)
        return True
    except Exception:
        return False
