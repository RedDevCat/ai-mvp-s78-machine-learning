import os
from pypdf import PdfReader
from docx import Document

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in {".txt", ".md"}:
        try:
            return open(path, "r", encoding="utf-8", errors="ignore").read()
        except:
            return open(path, "r", errors="ignore").read()
    if ext == ".pdf":
        try:
            reader = PdfReader(path)
            return "\n".join([p.extract_text() or "" for p in reader.pages])
        except:
            return ""
    if ext == ".docx":
        try:
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs])
        except:
            return ""
    try:
        return open(path, "r", encoding="utf-8", errors="ignore").read()
    except:
        return ""
