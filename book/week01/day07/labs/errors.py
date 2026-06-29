class LLMClientError(Exception):
    """Erreur générique du client LLM."""


class LLMConfigurationError(LLMClientError):
    """Erreur de configuration du client LLM."""


class LLMValidationError(LLMClientError):
    """Erreur de validation d'une sortie LLM."""
