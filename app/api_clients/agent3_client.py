"""
HTTP client for Agent 3 (ccai-gov-intelligence) FastAPI backend.
"""
import httpx
from app.config import AGENT3_URL, HTTP_TIMEOUT


def health_check() -> dict:
    """Returns {"status": "ok", "index_loaded": true/false}."""
    response = httpx.get(f"{AGENT3_URL}/health", timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json()


def classify_request(request_id: str, complaint_text: str) -> dict:
    """
    Classifies a 311 citizen complaint.
    Returns ClassificationResult: departments, urgency, work_orders, acknowledgment_letter.
    """
    response = httpx.post(
        f"{AGENT3_URL}/classify",
        json={"request_id": request_id, "complaint_text": complaint_text},
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def query_cjis(query_id: str, question: str) -> dict:
    """
    Queries the CJIS Security Policy RAG agent.
    Returns CJISQueryResult: answer, citations, cannot_answer flag.
    """
    response = httpx.post(
        f"{AGENT3_URL}/query-cjis",
        json={"query_id": query_id, "question": question},
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return response.json()
