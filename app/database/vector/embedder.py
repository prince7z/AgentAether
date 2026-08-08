"""Embeddings generator client utilizing BAAI/bge-small-en-v1.5 on the Infinity Server."""

import logging
import httpx

from app.config import Infinity_url

logger = logging.getLogger("openclaw-agent")


def _normalize_infinity_url(raw_url: str) -> str:
    """Strips trailing paths like /rerank, /v1/rerank, /embeddings, etc. to get the root server URL."""
    url = raw_url.rstrip("/")
    for suffix in ["/rerank", "/v1/rerank", "/embeddings", "/v1/embeddings"]:
        if url.endswith(suffix):
            url = url[:-len(suffix)].rstrip("/")
    return url


async def generate_embeddings(request_id: str, texts: list[str]) -> list[list[float]]:
    """Generate vector embeddings for a list of texts using the Infinity Embeddings API.

    Args:
        request_id: Unique request session identifier.
        texts: A list of string texts to embed.

    Returns:
        A list of vector embeddings (list of floats).
    """
    from app.tools.search.utils import log_stage
    log_stage(request_id, "🧠 Generating Embeddings...")

    if not texts:
        return []

    if not Infinity_url:
        log_stage(request_id, "Warning: INFINITY_URL is not configured. Returning empty vectors.", "warning")
        return [[] for _ in texts]

    base_url = _normalize_infinity_url(Infinity_url)
    url = f"{base_url}/embeddings"
    payload = {
        "model": "BAAI/bge-small-en-v1.5",
        "input": texts
    }

    response = None
    last_error = "timeout or connection failure"

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.post(url, json=payload)
            if res.status_code == 200:
                response = res
            else:
                last_error = f"status {res.status_code}: {res.text}"
        except Exception as exc:
            last_error = str(exc)
            logger.warning(f"Embedding failed on endpoint {url}: {exc}")

    if not response or response.status_code != 200:
        log_stage(
            request_id,
            f"Error: Embedding API call failed ({last_error}).",
            "error"
        )
        return [[] for _ in texts]

    data = response.json()
    raw_data = data.get("data") or []
    
    # Sort embeddings by original list index to preserve order
    sorted_data = sorted(raw_data, key=lambda item: item.get("index", 0))
    embeddings = [item["embedding"] for item in sorted_data]

    log_stage(request_id, f"🧠 Embedded {len(embeddings)} items successfully.")
    return embeddings
