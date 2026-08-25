"""Reranker client utilizing BAAI/bge-reranker-base on the Infinity Server with local fallback."""

import asyncio
import logging
from typing import TYPE_CHECKING, Any
import httpx

from app.config import Infinity_url

if TYPE_CHECKING:
    from app.tools.search.schemas import Chunk

logger = logging.getLogger("openclaw-agent")

_LOCAL_RERANKER_MODEL = None


def _normalize_infinity_url(raw_url: str) -> str:
    """Strips trailing paths like /rerank, /v1/rerank, /embeddings, etc. to get the root server URL."""
    url = raw_url.rstrip("/")
    for suffix in ["/rerank", "/v1/rerank", "/embeddings", "/v1/embeddings"]:
        if url.endswith(suffix):
            url = url[:-len(suffix)].rstrip("/")
    return url


def _get_local_reranker():
    global _LOCAL_RERANKER_MODEL
    if _LOCAL_RERANKER_MODEL is None:
        from sentence_transformers import CrossEncoder
        _LOCAL_RERANKER_MODEL = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    return _LOCAL_RERANKER_MODEL


def local_rerank(query: str, chunks: list[Any], top_k: int = 4) -> list[Any]:
    """Rerank chunks locally using sentence_transformers."""
    try:
        model = _get_local_reranker()
        pairs = [[query, chunk.content] for chunk in chunks]
        scores = model.predict(pairs)
        for chunk, score in zip(chunks, scores):
            chunk.score = float(score)
        sorted_chunks = sorted(chunks, key=lambda x: x.score, reverse=True)
        return sorted_chunks[:top_k]
    except Exception as e:
        logger.error(f"Local reranker failed: {e}")
        return chunks[:top_k]


async def rerank_chunks(
    request_id: str,
    query: str,
    chunks: list[Any],
    top_k: int = 5
) -> list[Any]:
    """Rerank chunks based on relevance to the query using the Infinity Reranker API.

    If the Infinity Reranker API fails, falls back to a local SentenceTransformers model.

    Args:
        request_id: Unique request session identifier.
        query: The search query.
        chunks: A list of candidate Chunk models.
        top_k: The number of top chunks to return.

    Returns:
        A list of the top_k reranked Chunk models sorted descending by relevance score.
    """
    from app.tools.search.utils import log_stage
    log_stage(request_id, "🎯 Reranking Chunks...")

    if not chunks:
        return []

    # Map chunks to their text content
    document_texts = [chunk.content for chunk in chunks]
    response = None
    last_error = "timeout or connection failure"

    if Infinity_url:
        base_url = _normalize_infinity_url(Infinity_url)
        # Primary endpoint for Infinity Server is /rerank
        url = f"{base_url}/rerank"
        payload = {
            "model": "BAAI/bge-reranker-base",
            "query": query,
            "documents": document_texts,
            "top_n": top_k
        }
        MAX_RETRIES = 2
        async with httpx.AsyncClient(timeout=5.0) as client:
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        res = await client.post(url, json=payload)
                        if res.status_code == 200:
                            response = res
                            break
                        else:
                            last_error = f"status {res.status_code}: {res.text}"
                            logger.warning(f"Reranker attempt {attempt} failed with status {res.status_code}: {res.text}")
                    except Exception as exc:
                        last_error = str(exc)
                        logger.warning(f"Reranker attempt {attempt} failed on endpoint {url}: {exc}")
                    if attempt < MAX_RETRIES:
                        await asyncio.sleep(0.5)  # brief pause before retry

    if not response or response.status_code != 200:
        log_stage(
            request_id,
            f"Warning: Remote Reranker failed ({last_error}). Falling back to local SentenceTransformers reranker...",
            "warning"
        )
        try:
            reranked_chunks = await asyncio.to_thread(local_rerank, query, chunks, top_k)
            log_stage(request_id, f"🎯 Local rerank completed. Returned top {len(reranked_chunks)} chunks.")
            return reranked_chunks
        except Exception as local_exc:
            log_stage(
                request_id,
                f"Error: Local reranker also failed ({local_exc}). Returning original chunks.",
                "error"
            )
            return chunks[:top_k]

    data = response.json()
    results = data.get("results") or []

    reranked_chunks = []
    for item in results:
        idx = item["index"]
        score = item["relevance_score"]
        
        # Retrieve the original chunk and assign the rerank score
        chunk = chunks[idx]
        chunk.score = score
        reranked_chunks.append(chunk)

    log_stage(request_id, f"🎯 Reranked to top {len(reranked_chunks)} chunks.")
    return reranked_chunks
