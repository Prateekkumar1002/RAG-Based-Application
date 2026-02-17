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

