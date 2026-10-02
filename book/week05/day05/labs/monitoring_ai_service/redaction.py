import re

EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
API_KEY_PATTERN = re.compile(r"\b(?:sk|pk|rk|api)[-_][A-Za-z0-9_\-]{8,}\b", re.IGNORECASE)
BEARER_PATTERN = re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]+", re.IGNORECASE)


def redact_sensitive_text(text: str) -> str:
    """Supprime les secrets les plus courants avant journalisation."""

    redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
    redacted = API_KEY_PATTERN.sub("[REDACTED_SECRET]", redacted)
    redacted = BEARER_PATTERN.sub("Bearer [REDACTED_SECRET]", redacted)
    return redacted
