from pypdf import PdfReader
from docx import Document


def load_pdf(file_path: str) -> str:
    """
    Read a PDF file and return all extracted text as a single string.
    """
    text = []

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def load_docx(file_path: str) -> str:
    """
    Read a DOCX file and return all extracted text as a single string.
    """
    doc = Document(file_path)
    text = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def load_document(file_path: str) -> str:
    """
    Detect file type and load text from PDF or DOCX.
    """
    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        return load_pdf(file_path)

    if file_path_lower.endswith(".docx"):
        return load_docx(file_path)

    raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")