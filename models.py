from dataclasses import dataclass
from email.mime import text
from enum import Enum
import re
from typing import Final

class ErrorCode(Enum):
    RATE_LIMIT = "RATE_LIMIT"
    MODEL_ERROR = "MODEL_ERROR"
    CONTEXT_OVERFLOW = "CONTEXT_OVERFLOW"
    AUTH_ERROR = "AUTH_ERROR"
    UNKNOWN = "UNKNOWN"

@dataclass
class InvocationResult:
    success: bool
    content: str | None = None
    error_code: ErrorCode = ErrorCode.UNKNOWN
    error_message: str | None = None
    attempts: int = 0
    