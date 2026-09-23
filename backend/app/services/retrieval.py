import re
import chromadb

from app.core.config import settings
from sentence_transformers import SentenceTransformer
from app.services.authorization import get_allowed_access_levels


# Global variables for models (loaded in lifespan)
_chroma_client = None
_collection = None
_embedding_model = None


def load_models():
    global _chroma_client, _collection, _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL_NAME
        )

    if _chroma_client is None:
        try:
            _chroma_client = chromadb.PersistentClient(
                path=settings.VECTOR_STORE_PATH
            )

            _collection = _chroma_client.get_collection(
                "school_knowledge"
            )

        except Exception as e:
            print(
                f"Warning: ChromaDB collection not found or error loading: {e}"
            )
            _collection = None


def _get_keywords(query: str) -> list[str]:
    """
    Extract meaningful keywords from the user's question.
    """

    stop_words = {
        "what",
        "are",
        "the",
        "is",
        "a",
        "an",
        "of",
        "in",
        "on",
        "to",
        "for",
        "and",
        "or",
        "does",
        "do",
        "how",
        "when",
        "where",
        "why",
        "which",
        "what's",
        "mentioned",
        "structure",
        "components",
    }

    words = re.findall(r"\b[a-zA-Z0-9'-]+\b", query.lower())

    keywords = [
        word
        for word in words
        if word not in stop_words and len(word) > 1
    ]

    return keywords


def _keyword_score(query: str, content: str) -> int:
    """
    Count how many meaningful query keywords appear in the chunk.
    """

    keywords = _get_keywords(query)
    content_lower = content.lower()

    score = 0

    for keyword in keywords:
        if keyword in content_lower:
            score += 1

    return score


def retrieve_chunks(
    query: str,
    user_role: str,
    top_k: int = 5
):
    if _collection is None:
        return []

    # Security: determine what this user is allowed to access
    allowed_levels = get_allowed_access_levels(user_role)

    if not allowed_levels:
        return []

    # Security filter BEFORE retrieval
    if len(allowed_levels) == 1:
        where_filter = {
            "access_level": allowed_levels[0]
        }
    else:
        where_filter = {
            "$or": [
                {"access_level": level}
                for level in allowed_levels
            ]
        }

    # Semantic retrieval
    query_embedding = _embedding_model.encode(
        [query]
    ).tolist()

    # Retrieve a slightly larger candidate set for reranking
    candidate_count = min(top_k * 2, _collection.count())

    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=candidate_count,
        where=where_filter
    )

    candidates = []

    if results and results.get("ids") and results["ids"][0]:

        for i in range(len(results["ids"][0])):

            content = results["documents"][0][i]

            semantic_distance = results["distances"][0][i]

            keyword_score = _keyword_score(
                query,
                content
            )

            candidates.append({
                "id": results["ids"][0][i],
                "content": content,
                "metadata": results["metadatas"][0][i],
                "semantic_distance": semantic_distance,
                "keyword_score": keyword_score,
            })

    # Rerank:
    # 1. Higher keyword match first
    # 2. Lower semantic distance second
    candidates.sort(
        key=lambda x: (
            -x["keyword_score"],
            x["semantic_distance"]
        )
    )

    retrieved = []

    for candidate in candidates[:top_k]:

        retrieved.append({
            "id": candidate["id"],
            "content": candidate["content"],
            "metadata": candidate["metadata"],
        })

    return retrieved