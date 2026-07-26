"""
HTTP client for Agent 1 (gcp-devops-compliance-agent) FastAPI backend.
All calls go through this module. Never call the backend URL directly from tabs.
"""
import httpx
from app.config import AGENT1_URL, HTTP_TIMEOUT


def health_check() -> dict:
    """Returns {"status": "ok"} or raises on failure."""
    response = httpx.get(f"{AGENT1_URL}/health", timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json()


def chat(query: str) -> dict:
    """
    Sends a natural language query to the DevOps compliance agent.
    Returns {"response": "string", "tools_called": ["list"]}.
    """
    response = httpx.post(
        f"{AGENT1_URL}/chat",
        json={"query": query},
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
