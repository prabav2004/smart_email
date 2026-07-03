import re
from typing import Dict, Any


def format_email_body(body: str) -> str:
    """
    Cleans raw email body text, removing extra spaces and standardizing linebreaks.
    """
    if not body:
        return ""
    # Normalize spacing and line endings
    cleaned = re.sub(r'\r\n', '\n', body)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


def validate_email_structure(email: Dict[str, Any]) -> bool:
    """
    Checks if email object has required keys to be processed.
    """
    required_keys = {"subject", "sender", "body"}
    return required_keys.issubset(email.keys())
