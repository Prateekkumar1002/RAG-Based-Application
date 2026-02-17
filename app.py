# import streamlit as st
# import uuid
# import time

# from core.document_loader import load_document
# from core.chunker import chunk_text
# from core.embeddings import get_embeddings
# from core.vectorstore import init_collection, upsert_chunks
# from core.rag_pipeline import ask_question

# st.set_page_config(page_title="Document Chat", layout="wide")

# # ---------------------------------------------------
# # 🔹 SESSION INITIALIZATION
# # ---------------------------------------------------

# if "sessions" not in st.session_state:
#     st.session_state.sessions = {}

# if "active_session" not in st.session_state:
#     st.session_state.active_session = None


# def create_new_session():
#     session_id = str(uuid.uuid4())

#     st.session_state.sessions[session_id] = {
#         "title": "New Chat",
#         "chat_history": [],
#         "uploaded": False
#     }

#     st.session_state.active_session = session_id


# # Create first session automatically
# if not st.session_state.sessions:
#     create_new_session()

# session_id = st.session_state.active_session
# current = st.session_state.sessions[session_id]

# # ---------------------------------------------------
# # 🔹 SIDEBAR (ChatGPT Style)
# # ---------------------------------------------------

# with st.sidebar:
#     st.title("💬 Document Chats")

#     if st.button("➕ New Chat"):
#         create_new_session()
#         st.rerun()

#     st.divider()

#     for sid, data in st.session_state.sessions.items():
#         title = data.get("title", "New Chat")

#         if st.button(title, key=sid):
#             st.session_state.active_session = sid
#             st.rerun()

# # ---------------------------------------------------
# # 🔹 MAIN HEADER
# # ---------------------------------------------------

# st.title("📄 Document Chat")

# # ---------------------------------------------------
# # 🔹 FILE UPLOAD
# # ---------------------------------------------------

# if not current["uploaded"]:

#     uploaded_file = st.file_uploader(
#         "Upload PDF / DOCX / TXT",
#         type=["pdf", "docx", "txt"]
#     )

#     if uploaded_file:

#         with st.spinner("Processing document..."):

#             # Load + Chunk
#             text = load_document(uploaded_file)
#             chunks = chunk_text(text)

#             # Batch embeddings
#             embeddings = get_embeddings(chunks)

#             # Initialize vector DB
#             init_collection()

#             # Store in Qdrant
#             upsert_chunks(chunks, embeddings, session_id)

#         # Update session
#         current["uploaded"] = True
#         current["title"] = uploaded_file.name
#         current["chat_history"] = []

#         st.success("Document indexed successfully ✅")
#         st.rerun()

# # ---------------------------------------------------
# # 🔹 CHAT INTERFACE
# # ---------------------------------------------------

# if current["uploaded"]:

#     # Display chat history
#     for message in current["chat_history"]:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # User input
#     question = st.chat_input("Ask something about your document...")

#     if question:

#         # Show user message
#         with st.chat_message("user"):
#             st.markdown(question)

#         current["chat_history"].append({
#             "role": "user",
#             "content": question
#         })

#         # Generate answer
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):

#                 start = time.time()

#                 # answer, latency = ask_question(
#                 #     question,
#                 #     session_id,
#                 #     current["chat_history"]
#                 # )
#                 answer, latency = ask_question(
#                     question,
#                     session_id,
#                     st.session_state.chat_history
#                 )


#                 end = time.time()

#                 st.markdown(answer)
#                 st.caption(f"⚡ {round(latency, 2)}s")

#         current["chat_history"].append({
#             "role": "assistant",
#             "content": answer
#         })



# import streamlit as st
# import uuid
# import time

# from core.document_loader import load_document
# from core.chunker import chunk_text
# from core.embeddings import get_embeddings
# from core.vectorstore import init_collection, upsert_chunks
# from core.rag_pipeline import ask_question

# # ----------------------------
# # Page Config
# # ----------------------------

# st.set_page_config(
#     page_title="Document Chat",
#     layout="wide",
# )

# st.title("📄 Document Chat")

# # ----------------------------
# # Session State Initialization
# # ----------------------------

# if "sessions" not in st.session_state:
#     st.session_state.sessions = {}

# if "current_session" not in st.session_state:
#     new_id = str(uuid.uuid4())
#     st.session_state.current_session = new_id
#     st.session_state.sessions[new_id] = {
#         "title": "New Chat",
#         "chat_history": [],
#         "uploaded": False,
#     }

# session_id = st.session_state.current_session
# current = st.session_state.sessions[session_id]

# # ----------------------------
# # Sidebar (ChatGPT Style)
# # ----------------------------

# with st.sidebar:
#     st.header("💬 Chats")

#     # New Chat Button
#     if st.button("➕ New Chat"):
#         new_id = str(uuid.uuid4())
#         st.session_state.current_session = new_id
#         st.session_state.sessions[new_id] = {
#             "title": "New Chat",
#             "chat_history": [],
#             "uploaded": False,
#         }
#         st.rerun()

#     st.divider()

#     # Existing Chats
#     for sid, data in st.session_state.sessions.items():
#         title = data.get("title", "Untitled")

#         if st.button(f"🗂 {title}", key=sid):
#             st.session_state.current_session = sid
#             st.rerun()

# # ----------------------------
# # File Upload Section
# # ----------------------------

# if not current["uploaded"]:

#     st.subheader("Upload PDF / DOCX / TXT")

#     uploaded_file = st.file_uploader(
#         "Drag and drop file here",
#         type=["pdf", "docx", "txt"],
#     )

#     if uploaded_file:

#         with st.spinner("Processing document..."):

#             text = load_document(uploaded_file)
#             chunks = chunk_text(text)

#             embeddings = get_embeddings(chunks)

#             init_collection()

#             upsert_chunks(
#                 chunks,
#                 embeddings,
#                 session_id,
#             )

#             # Set chat title from file name
#             current["title"] = uploaded_file.name
#             current["uploaded"] = True

#         st.success("Document indexed successfully!")
#         st.rerun()

# # ----------------------------
# # Chat Interface
# # ----------------------------

# if current["uploaded"]:

#     # Display Chat History
#     for msg in current["chat_history"]:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # User Input
#     question = st.chat_input("Ask something about the document...")

#     if question:

#         # Store user message
#         current["chat_history"].append(
#             {"role": "user", "content": question}
#         )

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):

#                 answer, latency, retrieved_chunks = ask_question(
#                     question,
#                     session_id,
#                     current["chat_history"],
#                 )

#                 st.markdown(answer)

#                 st.caption(
#                     f"""
# ⏱ Total: {latency['total']}s  
# Embedding: {latency['embedding']}s  
# Retrieval: {latency['retrieval']}s  
# Generation: {latency['generation']}s
# """
#                 )

#                 with st.expander("📚 Retrieved Context"):
#                     if retrieved_chunks:
#                         for chunk in retrieved_chunks:
#                             st.write(
#                                 f"Page {chunk['page']} | Score: {round(chunk['score'], 3)}"
#                             )
#                             st.write(chunk["text"])
#                             st.divider()
#                     else:
#                         st.write("No relevant context retrieved.")

#         # Store assistant message
#         current["chat_history"].append(
#             {"role": "assistant", "content": answer}
#         )




# import streamlit as st
# import uuid
# import time
# import hashlib

# # from core.loader import load_document
# from core.document_loader import load_document

# from core.chunker import chunk_text
# from core.embeddings import get_embeddings
# from core.vectorstore import init_collection, upsert_chunks
# from core.rag_pipeline import ask_question


# # -------------------------------------------------------
# # PAGE CONFIG
# # -------------------------------------------------------

# st.set_page_config(
#     page_title="📄 Document Chat",
#     page_icon="📄",
#     layout="wide"
# )


# # -------------------------------------------------------
# # SESSION STATE INIT
# # -------------------------------------------------------

# if "sessions" not in st.session_state:
#     st.session_state.sessions = {}

# if "current_session" not in st.session_state:
#     st.session_state.current_session = None


# # -------------------------------------------------------
# # SIDEBAR (ChatGPT Style)
# # -------------------------------------------------------

# with st.sidebar:

#     st.title("💬 Chats")

#     # New Chat Button
#     if st.button("➕ New Chat", use_container_width=True):
#         session_id = str(uuid.uuid4())

#         st.session_state.sessions[session_id] = {
#             "title": "New Chat",
#             "chat_history": [],
#             "uploaded": False
#         }

#         st.session_state.current_session = session_id

#     st.divider()

#     # Existing Chats
#     for session_id, data in st.session_state.sessions.items():

#         title = data.get("title", "Untitled Chat")

#         if st.button(f"📄 {title}", key=session_id, use_container_width=True):
#             st.session_state.current_session = session_id


# # -------------------------------------------------------
# # MAIN AREA
# # -------------------------------------------------------

# st.title("📄 Document Chat")

# if not st.session_state.current_session:
#     st.info("👈 Create or select a chat from sidebar to begin.")
#     st.stop()

# current_session_id = st.session_state.current_session
# current = st.session_state.sessions[current_session_id]


# doc_hash = hashlib.md5(text.encode()).hexdigest()

# if "indexed_docs" not in st.session_state:
#     st.session_state.indexed_docs = {}

# if doc_hash not in st.session_state.indexed_docs:
#     embeddings = get_embeddings(chunks)
#     init_collection()
#     upsert_chunks(chunks, embeddings, session_id)
#     st.session_state.indexed_docs[doc_hash] = True


# # -------------------------------------------------------
# # FILE UPLOAD
# # -------------------------------------------------------

# if not current["uploaded"]:

#     uploaded_file = st.file_uploader(
#         "Upload PDF / DOCX / TXT",
#         type=["pdf", "docx", "txt"]
#     )

#     if uploaded_file:

#         with st.spinner("Processing document..."):

#             # Load
#             text = load_document(uploaded_file)

#             # Chunk
#             chunks = chunk_text(text)

#             # Embed
#             embeddings = get_embeddings(chunks)

#             # Init Qdrant collection
#             init_collection()

#             # Upsert
#             upsert_chunks(chunks, embeddings, current_session_id)

#         # Update session
#         current["uploaded"] = True
#         current["title"] = uploaded_file.name
#         current["chat_history"] = []

#         st.success("✅ Document indexed successfully!")
#         st.rerun()

#     st.stop()


# # -------------------------------------------------------
# # DISPLAY CHAT HISTORY
# # -------------------------------------------------------

# for message in current["chat_history"]:

#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# # -------------------------------------------------------
# # CHAT INPUT
# # -------------------------------------------------------

# question = st.chat_input("Ask something about the document...")

# if question:

#     # 1️⃣ Append user message immediately
#     current["chat_history"].append({
#         "role": "user",
#         "content": question
#     })

#     # 2️⃣ Render user message instantly
#     with st.chat_message("user"):
#         st.markdown(question)

#     # 3️⃣ Generate assistant response
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):

#             start_time = time.time()

#             #answer, latency_data = ask_question(
#             answer, latency_data, context_chunks = ask_question(
#                 question,
#                 current_session_id,
#                 current["chat_history"]
#             )

#             total_time = round(time.time() - start_time, 2)

#             st.markdown(answer)

#             # Latency breakdown
#             st.caption(
#                 f"⏱ Total: {total_time}s | "
#                 f"Embedding: {latency_data.get('embedding', 0)}s | "
#                 f"Retrieval: {latency_data.get('retrieval', 0)}s | "
#                 f"Generation: {latency_data.get('generation', 0)}s"
#             )

#             # Show retrieved context
#             if "context" in latency_data:
#                 with st.expander("📚 Retrieved Context"):
#                     for item in latency_data["context"]:
#                         st.markdown(
#                             f"**Page {item.get('page', 'N/A')} | "
#                             f"Score: {round(item.get('score', 0), 3)}**"
#                         )
#                         st.write(item.get("text", ""))

#     # 4️⃣ Append assistant message
#     current["chat_history"].append({
#         "role": "assistant",
#         "content": answer
#     })








# import streamlit as st
# import hashlib
# import uuid
# import time

# # ---- CORE IMPORTS (Use your existing working core files) ----
# from core.document_loader import load_document
# from core.chunker import chunk_text
# from core.embeddings import get_embeddings
# from core.vectorstore import init_collection, upsert_chunks
# from core.rag_pipeline import ask_question

# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(
#     page_title="Document Chat",
#     page_icon="📄",
#     layout="wide"
# )

# # -----------------------------
# # Session Initialization
# # -----------------------------
# if "sessions" not in st.session_state:
#     st.session_state.sessions = {}

# if "current_session" not in st.session_state:
#     new_id = str(uuid.uuid4())
#     st.session_state.current_session = new_id
#     st.session_state.sessions[new_id] = {
#         "title": "New Chat",
#         "chat_history": [],
#         "indexed_docs": {}
#     }

# session_id = st.session_state.current_session
# current = st.session_state.sessions[session_id]

# # -----------------------------
# # Sidebar (ChatGPT Style)
# # -----------------------------
# with st.sidebar:

#     st.title("📂 Chats")

#     if st.button("➕ New Chat"):
#         new_id = str(uuid.uuid4())
#         st.session_state.current_session = new_id
#         st.session_state.sessions[new_id] = {
#             "title": "New Chat",
#             "chat_history": [],
#             "indexed_docs": {}
#         }
#         st.rerun()

#     st.markdown("---")

#     for sid, data in st.session_state.sessions.items():
#         if st.button(f"💬 {data['title']}", key=sid):
#             st.session_state.current_session = sid
#             st.rerun()

# # -----------------------------
# # Main Title
# # -----------------------------
# st.title("📄 Document Chat")

# # -----------------------------
# # File Upload
# # -----------------------------
# uploaded_file = st.file_uploader(
#     "Upload PDF/DOCX/TXT",
#     type=["pdf", "docx", "txt"]
# )

# if uploaded_file:

#     text = load_document(uploaded_file)

#     chunks = chunk_text(text)

#     # Generate document hash
#     doc_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

#     if doc_hash not in current["indexed_docs"]:

#         embeddings = get_embeddings(chunks)

#         init_collection()
#         upsert_chunks(chunks, embeddings, session_id)

#         current["indexed_docs"][doc_hash] = True

#         st.success("Document indexed successfully ✅")

#     else:
#         st.info("Document already indexed. Skipping re-embedding.")

# # -----------------------------
# # Chat Display
# # -----------------------------
# for message in current["chat_history"]:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # -----------------------------
# # Chat Input
# # -----------------------------
# question = st.chat_input("Ask something about your document...")

# if question:

#     # Add user message immediately (fixes invisible question issue)
#     current["chat_history"].append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.markdown(question)

#     # Assistant response
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):

#             start_time = time.time()

#             answer, latency_data = ask_question(
#                 question,
#                 session_id,
#                 current["chat_history"]
#             )

#             end_time = time.time()

#             total_time = round(end_time - start_time, 3)

#             st.markdown(answer)

#             st.markdown(
#                 f"""
# ⏱ **Total:** {total_time}s  
# Embedding: {latency_data.get("embedding", 0)}s  
# Retrieval: {latency_data.get("retrieval", 0)}s  
# Generation: {latency_data.get("generation", 0)}s
# """
#             )

#     current["chat_history"].append({
#         "role": "assistant",
#         "content": answer
#     })

#     # Auto title from first question
#     if current["title"] == "New Chat":
#         current["title"] = question[:40]

#     st.rerun()






import streamlit as st
import hashlib
import uuid
import time
import pandas as pd

# ---- CORE IMPORTS ----
from core.document_loader import load_document
from core.chunker import chunk_text
from core.embeddings import get_embeddings
from core.vectorstore import init_collection, upsert_chunks
from core.rag_pipeline import ask_question


# =============================
# EVALUATION QUESTIONS (ADD HERE)
# =============================
EVAL_QUESTIONS = [
    {
        "question": "What is Prateek's total experience?",
        "expected_keywords": ["2 years", "2+ years"]
    },
    {
        "question": "Which ML models were used in churn prediction?",
        "expected_keywords": ["Logistic", "Random Forest", "XGBoost"]
    },
    {
        "question": "What accuracy was achieved in election forecasting?",
        "expected_keywords": ["92%"]
    },
    {
        "question": "Which tools were used for web scraping?",
        "expected_keywords": ["Beautiful Soup", "Selenium"]
    },
    {
        "question": "Which NLP model was used for skill extraction?",
        "expected_keywords": ["BERT"]
    }
]


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Document Chat",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Initialize Session State
# -----------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_session = new_id
    st.session_state.sessions[new_id] = {
        "title": "New Chat",
        "chat_history": [],
        "indexed_docs": {}
    }

session_id = st.session_state.current_session
current = st.session_state.sessions[session_id]

# -----------------------------
# Sidebar (ChatGPT Style)
# -----------------------------
with st.sidebar:

    st.title("📂 Chats")

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.current_session = new_id
        st.session_state.sessions[new_id] = {
            "title": "New Chat",
            "chat_history": [],
            "indexed_docs": {}
        }
        st.rerun()

    st.markdown("---")

    for sid, data in st.session_state.sessions.items():
        title = data.get("title", "Untitled Chat")
        if st.button(f"💬 {title}", key=sid):
            st.session_state.current_session = sid
            st.rerun()

# -----------------------------
# Main Title
# -----------------------------
st.title("📄 Document Chat - RAG Based Q&A System")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload PDF/DOCX/TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    text_data = load_document(uploaded_file)
    chunks = chunk_text(text_data)

    # -----------------------------
    # SAFE HASHING (Fix encode error)
    # -----------------------------
    if isinstance(text_data, list):
        combined_text = ""
        for item in text_data:
            if isinstance(item, dict):
                combined_text += item.get("text", "")
            else:
                combined_text += str(item)
    elif isinstance(text_data, str):
        combined_text = text_data
    else:
        combined_text = str(text_data)

    doc_hash = hashlib.md5(
        combined_text.encode("utf-8")
    ).hexdigest()

    if doc_hash not in current["indexed_docs"]:

        with st.spinner("Indexing document..."):

            embeddings = get_embeddings(chunks)

            init_collection()
            upsert_chunks(chunks, embeddings, session_id)

            current["indexed_docs"][doc_hash] = True

        st.success("Document indexed successfully ✅")

    else:
        st.info("Document already indexed. Skipping re-embedding.")

# -----------------------------
# Display Chat History
# -----------------------------
for message in current["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
# question = st.chat_input("Ask something about your document...")

# if question:

#     # Add user message immediately (fix invisible message issue)
#     current["chat_history"].append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.markdown(question)

#     # Assistant response
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):

#             start_time = time.time()

#             # answer, latency_data = ask_question(
#             #     question,
#             #     session_id,
#             #     current["chat_history"]
#             # )

#             result = ask_question(
#                 question,
#                 session_id,
#                 current["chat_history"]
#             )

# # Handle different return formats safely
#             if isinstance(result, tuple):
#                 if len(result) == 2:
#                     answer, latency_data = result
#                     context_chunks = None
#                 elif len(result) == 3:
#                     answer, latency_data, context_chunks = result
#                 else:
#                     answer = result[0]
#                     latency_data = result[1] if len(result) > 1 else {}
#                     context_chunks = None
#             else:
#                 answer = result
#                 latency_data = {}
#                 context_chunks = None

#             end_time = time.time()
#             total_time = round(end_time - start_time, 3)

#             st.markdown(answer)

#             st.markdown(
#                 f"""
# ⏱ **Total:** {total_time}s  
# Embedding: {latency_data.get("embedding", 0)}s  
# Retrieval: {latency_data.get("retrieval", 0)}s  
# Generation: {latency_data.get("generation", 0)}s
# """
#             )

#     current["chat_history"].append({
#         "role": "assistant",
#         "content": answer
#     })

#     # Auto-generate title from first question
#     if current["title"] == "New Chat":
#         current["title"] = question[:40]

#     st.rerun()


question = st.chat_input("Ask something about your document...")

if question:

    current["chat_history"].append({
        "role": "user",
        "content": question
    })

    # Auto title from first user message
    if len(current["chat_history"]) == 1:
        current["title"] = question[:40]


    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            start_total = time.time()

            answer, latency_data = ask_question(
                question,
                session_id,
                current["chat_history"]
            )

            total_time = round(time.time() - start_total, 3)

            st.markdown(answer)

            st.markdown(
                f"""
⏱ **Total:** {total_time}s  
Embedding: {latency_data.get("embedding", 0)}s  
Retrieval: {latency_data.get("retrieval", 0)}s  
Generation: {latency_data.get("generation", 0)}s
"""
            )

    current["chat_history"].append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# -----------------------------
# Evaluation Section
# -----------------------------
st.markdown("---")
st.subheader("📊 Evaluation (Assignment Bonus)")

if st.button("Run Evaluation (5 Test Questions)"):

    results = []
    correct = 0

    for item in EVAL_QUESTIONS:

        question = item["question"]
        expected = item["expected_keywords"]

        answer, _ = ask_question(
            question,
            session_id,
            current["chat_history"]
        )

        # Check keyword presence
        matched = any(keyword.lower() in answer.lower() for keyword in expected)

        if matched:
            correct += 1

        results.append({
            "Question": question,
            "Expected Keywords": ", ".join(expected),
            "Model Answer": answer[:120] + "...",
            "Correct": "✅" if matched else "❌"
        })

    accuracy = round((correct / len(EVAL_QUESTIONS)) * 100, 2)

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

    st.success(f"Overall Accuracy: {accuracy}%")
