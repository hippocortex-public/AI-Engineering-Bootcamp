from __future__ import annotations

from dataclasses import dataclass

from .auth import Principal


class AccessDenied(Exception):
    pass


class ResourceNotFound(Exception):
    pass


def require_scope(principal: Principal, scope: str) -> None:
    if scope not in principal.scopes:
        raise AccessDenied


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant: str
    text: str


class DocumentStore:
    def __init__(self, documents: list[Document]) -> None:
        self._documents = {d.document_id: d for d in documents}
        if len(self._documents) != len(documents):
            raise ValueError("Duplicate document id")

    def get(self, principal: Principal, document_id: str) -> Document:
        require_scope(principal, "documents:read")
        document = self._documents.get(document_id)
        # Même réponse pour une ressource absente et pour celle d'un autre tenant.
        if document is None or document.tenant != principal.tenant:
            raise ResourceNotFound
        return document


class ToolPolicy:
    def authorize(self, principal: Principal, tool_name: str) -> None:
        require_scope(principal, "tools:read")
        if tool_name != "read_document":
            raise AccessDenied
