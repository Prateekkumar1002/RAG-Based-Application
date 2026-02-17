import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

COLLECTION_NAME = "rag_collection"
QDRANT_PATH = "./qdrant_storage"
EMBEDDING_DIM = 3072
