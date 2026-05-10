import re
from typing import Final

INJECTION_PATTERN: Final[list[str]] = [
    r"ignore|skip your| all| previous| past| earlier| prior| former| old| previous instructions",
   	r"system prompt.*disabled",
	r"new role",
	r"repeat.*system prompt",
	r"jailbreak",
    r"show me your system prompt",
]


#Layer 1 - input detection for prompt injection
def detect_injection(text: str) -> bool:
    """Return True if the input looks like a prompt injection attempt."""
    for pattern in INJECTION_PATTERN:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False