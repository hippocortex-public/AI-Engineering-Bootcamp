from monitoring_ai_service.redaction import redact_sensitive_text


def test_redact_email_and_api_key() -> None:
    text = "Contact alice@example.com with key sk-live-1234567890abcdef."
    redacted = redact_sensitive_text(text)

    assert "alice@example.com" not in redacted
    assert "sk-live-1234567890abcdef" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_SECRET]" in redacted


def test_redact_bearer_token() -> None:
    text = "Authorization: Bearer abc.def.ghi"
    assert redact_sensitive_text(text) == "Authorization: Bearer [REDACTED_SECRET]"
