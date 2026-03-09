import json
import os
import faiss
import numpy as np

from config import FAISS_INDEX_FILE, METADATA_FILE


def create_faiss_index(dimension: int):
    """
    Create a FAISS index using L2 distance.
    """
    index = faiss.IndexFlatL2(dimension)
    return index


def save_index(index, metadata: list[dict]):
    """
    Save FAISS index and metadata to disk.
    """
    os.makedirs(os.path.dirname(FAISS_INDEX_FILE), exist_ok=True)

    faiss.write_index(index, FAISS_INDEX_FILE)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_index():
    """
    Load FAISS index and metadata from disk.
    """
    if not os.path.exists(FAISS_INDEX_FILE):
        return None, []

    index = faiss.read_index(FAISS_INDEX_FILE)

    metadata = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    return index, metadata


def add_embeddings_to_index(embeddings: list[list[float]], metadata: list[dict]):
    """
    Create a new FAISS index from embeddings and save it.
    """
    if not embeddings:
        raise ValueError("No embeddings provided.")

    vectors = np.array(embeddings, dtype="float32")
    dimension = vectors.shape[1]

    index = create_faiss_index(dimension)
    index.add(vectors)

    save_index(index, metadata)


def search_similar_chunks(query_embedding: list[float], top_k: int = 3):
    """
    Search the most similar chunks in the FAISS index.
    """
    index, metadata = load_index()

    if index is None:
        return []

    query_vector = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        result = {
            "distance": float(distances[0][i]),
            "metadata": metadata[idx]
        }
        results.append(result)

    return results