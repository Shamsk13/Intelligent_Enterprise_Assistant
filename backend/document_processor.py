# backend/document_processor.py

import docx2txt
import PyPDF2
import tempfile
import yake

from transformers import pipeline

# Load summarization model once (HuggingFace)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

'''
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        return docx2txt.process(tmp_path)
    return ""
'''

import os

def extract_text(file):
    # If input is a string path, open the file first
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
            return docx2txt.process(tmp_path)
        return ""


def summarize_text(text):
    # Huggingface summarizer has length limits
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = " ".join(summarizer(chunk)[0]['summary_text'] for chunk in chunks[:3])
    return summary

def extract_keywords(text):
    kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]

def process_document(file):
    text = extract_text(file)
    if not text.strip():
        return "No readable text found.", []

    summary = summarize_text(text)
    keywords = extract_keywords(text)
    return summary, keywords





from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle

# Load Sentence Transformer model once
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def split_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks

def build_knowledge_base(chunks, save_path="models/knowledge_base.pkl"):
    vectors = embedder.encode(chunks)
    knowledge_base = list(zip(chunks, vectors))
    with open(save_path, "wb") as f:
        pickle.dump(knowledge_base, f)
    print(f"[INFO] Knowledge base saved at {save_path}")

'''
def split_text(text, max_length=500):
    sentences = text.split('. ')
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) <= max_length:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "
    if current:
        chunks.append(current.strip())
    return chunks
'''



from sentence_transformers import SentenceTransformer, util
import os



# Load HR content (preloaded from Google Employee Handbook)
'''
with open("data/Employee Handbook.docx", "r", encoding="utf-8") as f:
    HR_KNOWLEDGE = f.read()
'''


from backend.document_processor import extract_text
'''
with open("data/Employee Handbook.docx", "rb") as f:   # open as binary for docx
    HR_KNOWLEDGE = extract_text(f)
'''


HR_KNOWLEDGE = extract_text("data/Employee Handbook.docx")


# Break into chunks
HR_CHUNKS = [HR_KNOWLEDGE[i:i+500] for i in range(0, len(HR_KNOWLEDGE), 500)]

# Load SentenceTransformer model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute embeddings
CHUNK_EMBEDDINGS = embedder.encode(HR_CHUNKS, convert_to_tensor=True)

def query_knowledge_base(user_query):
    query_embedding = embedder.encode(user_query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, CHUNK_EMBEDDINGS, top_k=1)[0]
    top_chunk = HR_CHUNKS[hits[0]["corpus_id"]]
    return top_chunk


import faiss
import numpy as np
import os

def build_and_save_faiss_index(embeddings: np.ndarray, path: str):
    index = faiss.IndexFlatL2(embeddings.shape[1])  # Or use another index type
    index.add(embeddings)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)
build_and_save_faiss_index(CHUNK_EMBEDDINGS.cpu().detach().numpy(), "models/faiss_index")


def load_faiss_index(path="models/faiss_index"):
    if os.path.exists(path):
        index = faiss.read_index(path)
        return index
    else:
        raise FileNotFoundError(f"FAISS index not found at {path}")
def query_with_faiss(user_query):
    index = load_faiss_index()
    query_vec = embedder.encode([user_query])
    D, I = index.search(np.array(query_vec).astype("float32"), k=1)
    return HR_CHUNKS[I[0][0]]

