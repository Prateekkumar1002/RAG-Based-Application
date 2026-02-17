from google import genai
from config import GEMINI_API_KEY, EMBEDDING_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

# def get_embeddings(texts):
#     batch_size = 100
#     all_embeddings = []

#     for i in range(0, len(texts), batch_size):
#         batch = texts[i:i + batch_size]

#         response = client.models.embed_content(
#             model=EMBEDDING_MODEL,
#             contents=batch
#         )

#         for item in response.embeddings:
#             all_embeddings.append(item.values)

#     return all_embeddings

def get_embeddings(chunks):
    if isinstance(chunks[0], dict):
        texts = [chunk["text"] for chunk in chunks]
    else:
        texts = chunks

    embeddings = []

    for i in range(0, len(texts), 100):
        batch = texts[i:i + 100]

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch
        )

        for item in response.embeddings:
            embeddings.append(item.values)

    return embeddings
