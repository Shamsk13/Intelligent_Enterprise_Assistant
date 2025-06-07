import os
import tempfile
import docx2txt
import PyPDF2
import yake
from transformers import pipeline

# Load summarization model once (HuggingFace)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text(file):
    """
    Extract text from a given file path or file-like object.
    Supports PDF and DOCX.
    """
    # If input is a string (file path)
    if isinstance(file, str):
        ext = os.path.splitext(file)[1].lower()
        if ext == ".pdf":
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext == ".docx":
            return docx2txt.process(file)
        else:
            return ""
    else:
        # file-like object case
        if file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file.name.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            text = docx2txt.process(tmp_path)
            os.unlink(tmp_path)
            return text
        else:
            return ""

def summarize_text(text):
    """
    Summarize text in chunks due to model input length limits.
    """
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = " ".join(summarizer(chunk)[0]['summary_text'] for chunk in chunks[:3])
    return summary

def extract_keywords(text):
    """
    Extract keywords using YAKE.
    """
    kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]

def process_document(file):
    """
    Extract text, summarize and extract keywords.
    Returns summary and keywords list.
    """
    text = extract_text(file)
    if not text.strip():
        return "No readable text found.", []
    summary = summarize_text(text)
    keywords = extract_keywords(text)
    return summary, keywords

