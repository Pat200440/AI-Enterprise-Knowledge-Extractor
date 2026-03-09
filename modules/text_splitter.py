def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[str]:
    """
    Split text into overlapping chunks.

    Example:
    - chunk_size = 500
    - chunk_overlap = 50

    This means each new chunk starts 50 characters before
    the previous chunk ends.
    """
    if not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks