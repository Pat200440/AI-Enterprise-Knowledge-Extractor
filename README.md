# 🔍 AI Enterprise Knowledge Extractor

A local **Retrieval-Augmented Generation (RAG)** system that allows users to upload company documents and extract insights through natural language questions. Built with Python, Streamlit, Google Gemini AI, and FAISS.

---

## 📋 Project Description

**AI Enterprise Knowledge Extractor** is a document Q&A system that combines semantic search with AI-powered answer generation. Upload your PDF or DOCX files, and the system will:

- Extract and index document content
- Answer questions about your documents using natural language
- Provide answers with source references
- Run completely locally (only API calls to Gemini)

Perfect for querying company policies, technical documentation, research papers, or any collection of text documents.

---

## ✨ Features

- **Multi-format support**: Upload PDF and DOCX files
- **Semantic search**: Find relevant information using meaning, not just keywords
- **Source attribution**: View exact text chunks used to generate answers
- **Persistent storage**: Index documents once, query multiple times
- **Local processing**: All document processing happens on your machine
- **Easy-to-use interface**: Built with Streamlit for simplicity

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE FLOW                         │
└──────────────────────────────────────────────────────────────┘

  📄 Upload Documents (PDF/DOCX)
         │
         ▼
  📝 Extract Text
         │
         ▼
  ✂️  Split into Chunks (500 chars, 50 overlap)
         │
         ▼
  🧮 Generate Embeddings (Gemini API)
         │
         ▼
  💾 Store in FAISS Vector DB
         │
         ▼
  ❓ User Asks Question
         │
         ▼
  🔍 Embed Question → Search FAISS → Retrieve Top-K Chunks
         │
         ▼
  🤖 Send Context + Question to Gemini
         │
         ▼
  ✅ Generate Final Answer with Sources
```

### Core Components

- **Frontend**: Streamlit web interface
- **Embeddings**: Google Gemini API (`gemini-embedding-001`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **LLM**: Google Gemini API (`gemini-2.5-flash`)
- **Document Processing**: PyPDF and python-docx

---

## 📂 Project Structure

```
patrick_project/
│
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and environment setup
├── .env                        # API keys (not committed to git)
├── requirements.txt            # Python dependencies
│
├── modules/
│   ├── document_loader.py      # PDF/DOCX text extraction
│   ├── text_splitter.py        # Text chunking with overlap
│   ├── embeddings.py           # Gemini embedding generation
│   ├── vector_store.py         # FAISS index management
│   └── chat_engine.py          # RAG pipeline orchestration
│
└── data/
    ├── documents/              # Uploaded documents
    └── vector_store/           # FAISS index + metadata
        ├── faiss_index.bin
        └── metadata.json
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd patrick_project
```

2. **Create a virtual environment**

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**Required packages**:
```
streamlit
google-genai
python-dotenv
pypdf
python-docx
faiss-cpu
numpy
```

---

## ⚙️ Configuration

### Set up your API key

1. **Create a `.env` file** in the project root:

```bash
touch .env
```

2. **Add your Gemini API key**:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Add `.env` to `.gitignore`**:

```gitignore
.env
data/documents/*
data/vector_store/*
__pycache__/
*.pyc
```

### Optional: Customize settings in `config.py`

```python
# Models
GENERATION_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

# Chunk settings
CHUNK_SIZE = 500          # Characters per chunk
CHUNK_OVERLAP = 50        # Overlap between chunks
```

---

## 🎯 Running the Application

**Start the Streamlit app**:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔧 How the System Works

### 1️⃣ Document Loading
- Extracts text from PDF (using `pypdf`) or DOCX (using `python-docx`)

### 2️⃣ Text Chunking
- Splits documents into 500-character chunks with 50-character overlap
- Overlap ensures continuity between chunks

### 3️⃣ Embedding Generation
- Converts each chunk into a 768-dimensional vector using Gemini's embedding model
- Semantically similar text produces similar vectors

### 4️⃣ Vector Storage
- Stores embeddings in a FAISS index (`IndexFlatL2`)
- Metadata (source file, chunk ID, original text) saved separately as JSON

### 5️⃣ Query Processing
When you ask a question:
1. Question is converted to an embedding
2. FAISS finds the top-3 most similar chunks (by L2 distance)
3. Retrieved chunks are combined into context

### 6️⃣ Answer Generation
- Context + question sent to Gemini (`gemini-2.5-flash`)
- Gemini generates a natural answer based only on retrieved context
- Answer returned with source references

---

## 💡 Example Usage

### Step-by-Step Walkthrough

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Upload documents**
   - Click "Browse files" and select PDF/DOCX files
   - Example: `employee_handbook.pdf`, `company_policies.docx`

3. **Process documents**
   - Click "Process documents"
   - System extracts text → chunks → embeds → indexes

4. **Ask questions**
   - Type: _"What is the vacation policy?"_
   - Click "Ask"
   - View answer + source chunks

5. **Continue asking**
   - Index is persistent—no need to re-upload

### Sample Questions

- _"What are the remote work policies?"_
- _"Summarize the Q3 financial results"_
- _"What are the steps for expense reimbursement?"_
- _"Who is the contact person for IT support?"_

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Web interface framework |
| **Google Gemini API** | Embeddings (`gemini-embedding-001`) and text generation (`gemini-2.5-flash`) |
| **FAISS** | High-performance vector similarity search |
| **PyPDF** | PDF text extraction |
| **python-docx** | DOCX text extraction |
| **NumPy** | Numerical operations for embeddings |

---

## 🚧 Possible Improvements

### Short-term
- [ ] Add document summarization feature
- [ ] Implement batch processing for large files
- [ ] Support additional formats (TXT, Markdown, HTML)
- [ ] Add document version tracking

### Medium-term
- [ ] Implement semantic chunking (respect paragraphs/sections)
- [ ] Add hybrid search (combine embeddings + keyword search)
- [ ] Create chat history with conversation memory
- [ ] Add user authentication and access control

### Advanced
- [ ] Multi-language support with translation
- [ ] Fine-tune embeddings on domain-specific data
- [ ] Deploy as Docker container
- [ ] Add analytics dashboard for query tracking
- [ ] Implement incremental indexing (add/remove documents)

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and modify for your own projects.

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

## 📧 Contact

For questions or suggestions, please open an issue or reach out via [your contact method].

---

**⭐ If you find this project useful, please consider giving it a star!**
