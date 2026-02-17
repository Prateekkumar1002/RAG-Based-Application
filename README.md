📄 Document Chat – RAG Based Application

Overview

This project is a Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload any PDF, DOCX and TXT files and chat with it.

The system extracts text from the uploaded files, chunks it, generates embeddings, stores them in a vector database, retrieves relevant context, and generates grounded answers with citations.

The app supports follow-up questions using persistent chat history.

🏗 Architecture Flow

PDF Upload → Text Extraction → Chunking → Embeddings → Vector Store → Retrieval → Grounded Answer with Citations

🧠 Tech Stack

1) Component	Technology Used

1. UI:	Streamlit

2. LLM:	Gemini 2.5 Flash

3. Embeddings:	gemini-embedding-001 (3072 dimensions)

4. Vector DB:	Qdrant (local mode)

5. Retrieval:	Cosine Similarity Top-K

6. Language:	Python 3.10+


Processing Pipeline

1️⃣ Document Upload

-- User uploads a single file via Streamlit.

-- File is processed in memory.

2️⃣ Text Extraction

-- Uses Python based extraction.

-- Preserves page numbers for citation support.

-- Each chunk retains: Text & Page number

3️⃣ Chunking Strategy

-- Chunk size: ~800 characters

-- Overlap: ~100 characters

-- Strategy: Sliding window

Reason: Maintains semantic continuity and Reduces context loss

-- Optimized for embedding model token limits

4️⃣ Embeddings

-- Model: gemini-embedding-001

-- Dimension: 3072

Why: 

-- High-quality semantic embeddings

-- Native compatibility with Gemini ecosystem

-- Strong retrieval performance

5️⃣ Vector Store

-- Database: Qdrant (Local Mode)

-- Collection initialized dynamically

-- Vector size = 3072

-- Distance metric = Cosine Similarity

-- Points include metadata:

-- page number & text snippet

-- session id

Reason: Lightweight, Fast local development & Production-ready scalable architecture

6️⃣ Retrieval Strategy

-- Top-K = 5

-- Cosine similarity search

-- Filter by session_id to isolate documents per chat

Why:

-- Ensures only relevant document chunks are retrieved

-- Supports multiple chat sessions

7️⃣ RAG (Q&A Generation)

Prompt includes:

-- Retrieved context chunks

-- Page numbers

-- User question

-- Chat history (for follow-ups)

Rules enforced:

-- Answers must be grounded in context

-- Must include page citations

-- If information not found → respond accordingly

Features

✅ Upload any single File

✅ Chat interface

✅ Persistent conversation history

✅ Follow-up question support

✅ Page citations in answers

✅ Latency breakdown (Embedding / Retrieval / Generation)

✅ Multi-chat sidebar (ChatGPT style)

✅ Automatic chat renaming

✅ Evaluation table (5-question test)

🧪 Evaluation (Basic Accuracy Test)

The app includes 5 test sample questions:

Question	Expected Keywords	Result

Total experience?	2+ years	✅

Churn models used?	Logistic, Random Forest, XGBoost	✅

Election forecasting accuracy?	92%	✅

Web scraping tools?	Beautiful Soup, Selenium	✅

Skill extraction model?	BERT	✅

Accuracy: 100% on internal test document

🚀 How to Run Locally

1️⃣ Clone the repository

git clone <your-repo-url>

cd pdf-rag-app

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Set Environment Variable

Create a .env file:

GEMINI_API_KEY=your_api_key_here

OR export directly:

export GEMINI_API_KEY=your_key   # Mac/Linux

setx GEMINI_API_KEY your_key     # Windows

4️⃣ Run the app

streamlit run app.py

App will open at:

http://localhost:8501

📂 Project Structure
pdf-rag-app/

│

├── app.py

├── requirements.txt

├── README.md

│

└── core/

    ├── document_loader.py
    
    ├── chunker.py
    
    ├── embeddings.py
    
    ├── vectorstore.py
    
    ├── retriever.py
    
    ├── rag_pipeline.py
    
    └── prompt.py

✅ Requirements Coverage

Upload any file	✅

Persistent chat	✅

Show citations	✅

Sensible chunking	✅

Mention embedding model + dimension	✅

Vector DB used	✅

Retrieval strategy explained	✅

Grounded RAG prompt	✅

Follow-up handling	✅

streamlit run works	✅

Modular code	✅

Basic evaluation	✅

Edge Case Handling

-- Re-uploading same document skips re-indexing

-- Handles empty retrieval results

-- Prevents cross-session contamination

-- Avoids crashes on missing context

-- Graceful quota handling
