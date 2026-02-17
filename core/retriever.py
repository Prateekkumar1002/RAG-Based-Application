


from core.vectorstore import get_client
from config import COLLECTION_NAME
from qdrant_client.models import Filter, FieldCondition, MatchValue


def retrieve(query_embedding, session_id, top_k=5, score_threshold=0.4):
    """
    Retrieve top-k relevant chunks from Qdrant
    filtered by session_id.

    Returns:
        List[dict] with:
        {
            "text": str,
            "page": int,
            "score": float
        }
    """

    client = get_client()

    # Filter by session_id so each document has isolated memory
    search_filter = Filter(
        must=[
            FieldCondition(
                key="session_id",
                match=MatchValue(value=session_id)
            )
        ]
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        query_filter=search_filter
    )

    if not results.points:
        return []

    retrieved_chunks = []

    for hit in results.points:
        if hit.score >= score_threshold:
            retrieved_chunks.append({
                "text": hit.payload.get("text", ""),
                "page": hit.payload.get("page", "N/A"),
                "score": round(hit.score, 3)
            })

    return retrieved_chunks

