

import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from config import COLLECTION_NAME, EMBEDDING_DIM

# Persistent local storage
_client = QdrantClient(path="./qdrant_storage")


# ----------------------------
# Return Qdrant client
# ----------------------------
def get_client():
    return _client


# ----------------------------
# Create collection if missing
# ----------------------------
def init_collection():
    collections = [c.name for c in _client.get_collections().collections]

    if COLLECTION_NAME not in collections:
        _client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            ),
        )


# ----------------------------
# Upsert chunks
# ----------------------------
def upsert_chunks(chunks, embeddings, session_id):
    points = []

    for chunk, vector in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "page": chunk.get("page", "N/A"),
                    "session_id": session_id
                }
            )
        )

    _client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# ----------------------------
# Search function
# ----------------------------
# def search(query_embedding, session_id, top_k=5):

#     results = _client.query_points(
#         collection_name=COLLECTION_NAME,
#         query=query_embedding,
#         limit=top_k,
#         query_filter=Filter(
#             must=[
#                 FieldCondition(
#                     key="session_id",
#                     match=MatchValue(value=session_id)
#                 )
#             ]
#         )
#     )

#     return results.points

from qdrant_client.models import Filter, FieldCondition, MatchValue

def search(query_embedding, session_id, top_k=5):
    results = _client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="session_id",
                    match=MatchValue(value=session_id)
                )
            ]
        )
    )

    formatted = []

    for point in results.points:
        formatted.append({
            "text": point.payload["text"],
            "page": point.payload.get("page", "N/A"),
            "score": point.score
        })

    return formatted

