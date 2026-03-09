from google import genai
from config import GEMINI_API_KEY, EMBEDDING_MODEL


def get_genai_client():
    """
    Create and return a Gemini client.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def embed_text(text: str) -> list[float]:
    """
    Generate an embedding for a single text.
    """
    client = get_genai_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple text chunks.
    """
    client = get_genai_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )

    return [item.values for item in response.embeddings]