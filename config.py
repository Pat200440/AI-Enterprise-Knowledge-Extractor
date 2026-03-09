import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Models
GENERATION_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

# Chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Data folders
DOCUMENTS_DIR = "data/documents"
VECTOR_STORE_DIR = "data/vector_store"

# FAISS files
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
METADATA_FILE = os.path.join(VECTOR_STORE_DIR, "metadata.json")