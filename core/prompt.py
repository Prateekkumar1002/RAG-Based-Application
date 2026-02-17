# def build_prompt(context_chunks, question, chat_history=None):
#     """
#     context_chunks: list[str] OR list[dict]
#     chat_history: list of {"role": ..., "content": ...}
#     """

#     # Handle dict or string safely
#     processed_chunks = []

#     for chunk in context_chunks:
#         if isinstance(chunk, dict):
#             processed_chunks.append(chunk.get("text", ""))
#         else:
#             processed_chunks.append(str(chunk))

#     context = "\n\n".join(processed_chunks)

#     history_text = ""

#     if chat_history:
#         for msg in chat_history:
#             history_text += f"{msg['role'].upper()}: {msg['content']}\n"

#     prompt = f"""
# You are a document QA assistant.

# Answer ONLY using the provided context.
# If the answer is not in the context, say:
# "I cannot find this in the document."

# Context:
# {context}

# Conversation:
# {history_text}

# Question:
# {question}

# Answer:
# """

#     return prompt



# def build_prompt(context_chunks, question):
#     if not context_chunks:
#         return f"""
# You are a professional AI assistant.

# The document does not contain relevant information to answer the question.

# Question:
# {question}

# Answer:
# The information is not available in the document.
# """

#     context = ""

#     for chunk in context_chunks:
#         context += f"[Page {chunk['page']}]\n{chunk['text']}\n\n"

#     return f"""
# You are a professional AI assistant.

# Answer ONLY from the provided context.
# If the answer is not in the context, say:
# "The information is not available in the document."

# Provide structured bullet points if appropriate.
# Cite page numbers when possible.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """






# def build_prompt(context_chunks, question, chat_history=None):
#     """
#     Build RAG prompt using retrieved chunks.

#     context_chunks: List[dict]
#         [
#             {
#                 "text": "...",
#                 "page": 2,
#                 "score": 0.82
#             }
#         ]

#     chat_history: List[dict]
#         [
#             {"role": "user", "content": "..."},
#             {"role": "assistant", "content": "..."}
#         ]
#     """

#     # ---------- Format Context Properly ----------
#     if not context_chunks:
#         formatted_context = "No relevant context found."
#     else:
#         formatted_parts = []
#         for chunk in context_chunks:
#             text = chunk.get("text", "")
#             page = chunk.get("page", "N/A")
#             formatted_parts.append(
#                 f"[Page {page}]\n{text}"
#             )
#         formatted_context = "\n\n".join(formatted_parts)

#     # ---------- Format Chat History ----------
#     history_text = ""
#     if chat_history:
#         history_lines = []
#         for msg in chat_history[-5:]:  # last 5 exchanges only
#             role = msg.get("role", "")
#             content = msg.get("content", "")
#             history_lines.append(f"{role.upper()}: {content}")
#         history_text = "\n".join(history_lines)

#     # ---------- Final Prompt ----------
#     prompt = f"""
# You are a professional AI document assistant.

# STRICT RULES:
# 1. Answer ONLY using the provided context.
# 2. If answer is not found in the context, say:
#    "The document does not contain relevant information to answer this."
# 3. Always cite page numbers like (Page X).
# 4. Do NOT fabricate page numbers.
# 5. Be concise and professional.

# --------------------
# Conversation History:
# {history_text}

# --------------------
# Context:
# {formatted_context}

# --------------------
# Question:
# {question}

# Answer:
# """

#     return prompt.strip()




def build_prompt(context_chunks, question):
    """
    context_chunks = [
        {"text": "...", "page": 1, "score": 0.82}
    ]
    """

    if not context_chunks:
        return None  # handled outside

    formatted_context = []

    for chunk in context_chunks:
        text = chunk["text"]
        page = chunk.get("page", "N/A")
        score = round(chunk.get("score", 0), 3)

        formatted_context.append(
            f"{text}\n(Source: Page {page} | Similarity: {score})"
        )

    context_block = "\n\n".join(formatted_context)

    prompt = f"""
You are a helpful AI assistant.

Use ONLY the provided context to answer the question.
If the answer is not found in the context, say:
"The document does not contain relevant information to answer this."

Context:
{context_block}

Question:
{question}

Answer:
"""

    return prompt
