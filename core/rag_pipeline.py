# import time
# from google import genai
# from config import GEMINI_API_KEY, LLM_MODEL
# from core.retriever import retrieve
# from core.prompt import build_prompt
# from core.embeddings import get_embeddings

# client = genai.Client(api_key=GEMINI_API_KEY)


# def ask_question(question, session_id, chat_history):
#     start = time.time()

#     # Embed query
#     query_embedding = get_embeddings([question])[0]

#     # Retrieve context
#     context_chunks = retrieve(query_embedding, session_id)

#     # Build prompt
#     prompt = build_prompt(context_chunks, question, chat_history)

#     # Call Gemini
#     response = client.models.generate_content(
#         model=LLM_MODEL,
#         contents=prompt
#     )

#     latency = time.time() - start

#     return response.text, latency


# import time
# from google import genai
# from config import GEMINI_API_KEY, LLM_MODEL
# from core.embeddings import get_embeddings
# from core.retriever import retrieve
# from core.prompt import build_prompt


# client = genai.Client(api_key=GEMINI_API_KEY)


# def ask_question(question, session_id, chat_history):

#     total_start = time.time()

#     # 1️⃣ Embed question
#     embed_start = time.time()
#     query_embedding = get_embeddings([question])[0]
#     embed_time = time.time() - embed_start

#     # 2️⃣ Retrieve context
#     retrieve_start = time.time()
#     # context_chunks = retrieve(query_embedding, session_id)
#     context_chunks = retrieve(query_embedding, session_id)

# # Limit to top 3 chunks (prevents long prompts)
#     context_chunks = context_chunks[:3]

#     retrieve_time = time.time() - retrieve_start

#     # 3️⃣ Build prompt
#     prompt = build_prompt(context_chunks, question)

#     # 4️⃣ Generate answer
#     gen_start = time.time()
#     response = client.models.generate_content(
#         model=LLM_MODEL,
#         contents=prompt
#     )
#     gen_time = time.time() - gen_start

#     total_time = time.time() - total_start

#     answer = response.text if hasattr(response, "text") else str(response)

#     latency = {
#         "embedding": round(embed_time, 3),
#         "retrieval": round(retrieve_time, 3),
#         "generation": round(gen_time, 3),
#         "total": round(total_time, 3),
#     }

#     return answer, latency, context_chunks



import time
from google import genai
from config import GEMINI_API_KEY, LLM_MODEL
from core.retriever import retrieve
from core.prompt import build_prompt
from core.embeddings import get_embeddings

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_question(question, session_id, chat_history):

    latency = {}

    # -----------------------
    # 1️⃣ Embedding
    # -----------------------
    start = time.time()
    query_embedding = get_embeddings([question])[0]
    latency["embedding"] = round(time.time() - start, 3)

    # -----------------------
    # 2️⃣ Retrieval
    # -----------------------
    start = time.time()
    context_chunks = retrieve(query_embedding, session_id)
    latency["retrieval"] = round(time.time() - start, 3)

    # -----------------------
    # 3️⃣ Prompt Building
    # -----------------------
    prompt = build_prompt(context_chunks, question)

    # -----------------------
    # 4️⃣ Generation
    # -----------------------
    start = time.time()

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    latency["generation"] = round(time.time() - start, 3)

    answer = response.text

    return answer, latency
