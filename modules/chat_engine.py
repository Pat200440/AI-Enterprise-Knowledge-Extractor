from google import genai

from config import GEMINI_API_KEY, GENERATION_MODEL
from modules.embeddings import embed_text
from modules.vector_store import search_similar_chunks


def get_genai_client():
    """
    Create and return a Gemini client.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def build_context(results: list[dict]) -> str:
    """
    Build a context string from retrieved chunks.
    """
    context_parts = []

    for i, item in enumerate(results, start=1):
        chunk_text = item["metadata"].get("text", "")
        source = item["metadata"].get("source", "Unknown source")

        context_parts.append(
            f"Source {i}: {source}\n"
            f"Content:\n{chunk_text}\n"
        )

    return "\n".join(context_parts)


def answer_question(question: str, top_k: int = 3) -> dict:
    """
    Full retrieval + generation pipeline:
    1. Embed question
    2. Search similar chunks
    3. Build context
    4. Ask Gemini for final answer
    """
    client = get_genai_client()

    query_embedding = embed_text(question)
    results = search_similar_chunks(query_embedding, top_k=top_k)

    if not results:
        return {
            "answer": "No indexed documents found. Please upload and process documents first.",
            "sources": []
        }

    context = build_context(results)

    prompt = f"""
You are an assistant that answers questions using the provided company documents.

Use only the context below to answer.
If the answer is not present in the context, say that the information was not found in the uploaded documents.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": results
    }