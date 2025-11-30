from __future__ import annotations

from typing import Any, Dict, List

import requests


class HttpApiClient:
    @staticmethod
    def _send_post_request(
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str] | None = None,
        timeout: int = 30,
    ) -> Dict[str, Any] | str:
        """
        Core helper for issuing POST requests and parsing responses.
        Shared by the RAG and Retriever clients to keep behavior consistent.
        """
        try:
            headers = headers or {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.RequestException as exc:
            print(f"❌ Request failed: {exc}")
            raise

class PracticeStatementRagClient(HttpApiClient):

    def __init__(self, endpoint_root: str):
        self.endpoint_root: str = endpoint_root
        self.invoke_endpoint: str = f"{endpoint_root}/query"
    
    def invoke(self, query: str, timeout: int = 30):
        response = self._send_post_request(self.invoke_endpoint, {"query": query}, timeout=timeout)
        if not (answer := response.get("answer")):
            raise ValueError()
        return answer

class PracticeStatementRetrieverClient(HttpApiClient):
    """Thin wrapper around the retriever API."""

    def __init__(self, endpoint_root: str):
        self.endpoint_root: str = endpoint_root.rstrip("/")
        self.retrieve_endpoint: str = f"{self.endpoint_root}/retrieve"

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        timeout: int = 30,
    ) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {"query": query}
        if top_k is not None:
            if top_k <= 0:
                raise ValueError("top_k must be greater than zero")
            payload["top_k"] = top_k

        response = self._send_post_request(self.retrieve_endpoint, payload, timeout=timeout)
        if not isinstance(response, dict):
            raise ValueError("Retriever response was not valid JSON")

        documents = response.get("documents")
        if documents is None:
            raise ValueError("Retriever response missing 'documents'")
        if not isinstance(documents, list):
            raise ValueError("Retriever 'documents' field must be a list")

        return documents
