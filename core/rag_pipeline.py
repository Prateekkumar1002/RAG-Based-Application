
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

