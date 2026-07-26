"""
HTTP client for Agent 2 (ccai-quality-agent) FastAPI backend.
"""
import httpx
from app.config import AGENT2_URL, HTTP_TIMEOUT


def health_check() -> dict:
    response = httpx.get(f"{AGENT2_URL}/health", timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json()


def analyze_transcript(
    call_id: str,
    transcript_text: str,
    agent_id: str = "AGENT-001",
    queue_name: str = "general"
) -> dict:
    """
    Sends a call transcript for PCI compliance analysis + quality scoring.
    Returns full result: pci_result, scorecard, ticket (nullable), cached flag.
    """
    response = httpx.post(
        f"{AGENT2_URL}/analyze",
        json={
            "call_id": call_id,
            "transcript_text": transcript_text,
            "agent_id": agent_id,
            "queue_name": queue_name
        },
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
