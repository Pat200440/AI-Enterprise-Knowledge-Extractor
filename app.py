import os
import streamlit as st

from config import (
    GEMINI_API_KEY,
    DOCUMENTS_DIR,
    VECTOR_STORE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from modules.document_loader import load_document
from modules.text_splitter import split_text
from modules.embeddings import embed_texts
from modules.vector_store import add_embeddings_to_index
from modules.chat_engine import answer_question

# --------------------------------------------------
# Initial setup
# --------------------------------------------------

os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

st.set_page_config(
    page_title="AI Enterprise Knowledge Extractor",
    layout="wide"
)

st.title("AI Enterprise Knowledge Extractor")

col1, col2, col3 = st.columns(3)

with col2:
    st.image(image=r"C:\Users\Patrick\Desktop\patrick_project\data\ChatGPT Image Mar 7, 2026, 11_13_38 AM.png")

st.write("Upload company documents, index them, and ask questions about their content.")

# --------------------------------------------------
# API key check
# --------------------------------------------------

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please add it inside the .env file.")
    st.stop()

st.success("Gemini API key loaded successfully.")

# --------------------------------------------------
# Session state
# --------------------------------------------------

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []

# --------------------------------------------------
# File upload section
# --------------------------------------------------

st.header("1. Upload documents")

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Uploaded files: {len(uploaded_files)}")

# --------------------------------------------------
# Document processing section
# --------------------------------------------------

st.header("2. Process documents")

if st.button("Process documents"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF or DOCX file.")
    else:
        all_chunks = []
        all_metadata = []

        with st.spinner("Processing documents..."):
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                save_path = os.path.join(DOCUMENTS_DIR, file_name)

                # Save uploaded file locally
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract text
                try:
                    document_text = load_document(save_path)
                except Exception as e:
                    st.error(f"Error reading {file_name}: {e}")
                    continue

                if not document_text.strip():
                    st.warning(f"No text found inside {file_name}.")
                    continue

                # Split into chunks
                chunks = split_text(
                    text=document_text,
                    chunk_size=CHUNK_SIZE,
                    chunk_overlap=CHUNK_OVERLAP
                )

                # Save chunks + metadata
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadata.append(
                        {
                            "source": file_name,
                            "chunk_id": i,
                            "text": chunk
                        }
                    )

        if not all_chunks:
            st.error("No valid text chunks were created.")
        else:
            try:
                with st.spinner("Generating embeddings and saving to FAISS..."):
                    embeddings = embed_texts(all_chunks)
                    add_embeddings_to_index(embeddings, all_metadata)

                st.session_state.documents_processed = True
                st.session_state.last_uploaded_files = [f.name for f in uploaded_files]

                st.success("Documents processed and indexed successfully.")
                st.write(f"Total chunks created: {len(all_chunks)}")

            except Exception as e:
                st.error(f"Error during embedding/indexing: {e}")

# --------------------------------------------------
# Chat section
# --------------------------------------------------

st.header("3. Ask questions about your documents")

if st.session_state.documents_processed:
    st.info("Documents are ready. You can now ask questions.")
else:
    st.warning("Upload and process documents first.")

question = st.text_input("Write your question here")

if st.button("Ask"):
    if not st.session_state.documents_processed:
        st.warning("Please process documents before asking a question.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching relevant chunks and generating answer..."):
                result = answer_question(question)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Retrieved sources")
            if result["sources"]:
                for i, item in enumerate(result["sources"], start=1):
                    metadata = item["metadata"]

                    st.markdown(f"**Source {i}**")
                    st.write(f"**File:** {metadata.get('source', 'Unknown')}")
                    st.write(f"**Chunk ID:** {metadata.get('chunk_id', 'N/A')}")
                    st.write("**Chunk text:**")
                    st.code(metadata.get("text", ""), language="text")
                    st.write(f"**Distance:** {item.get('distance', 'N/A')}")
                    st.markdown("---")
            else:
                st.write("No sources found.")

        except Exception as e:
            st.error(f"Error while answering the question: {e}")

# --------------------------------------------------
# Sidebar info
# --------------------------------------------------

with st.sidebar:
    st.header("Project info")
    st.write("Simple local RAG with:")
    st.write("- Streamlit")
    st.write("- Gemini API")
    st.write("- Embeddings")
    st.write("- FAISS")

    st.header("Chunk settings")
    st.write(f"Chunk size: {CHUNK_SIZE}")
    st.write(f"Chunk overlap: {CHUNK_OVERLAP}")

    if st.session_state.last_uploaded_files:
        st.header("Last indexed files")
        for file_name in st.session_state.last_uploaded_files:
            st.write(f"- {file_name}")