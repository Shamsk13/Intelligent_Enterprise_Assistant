#backend/knowledge_base_builder.py
import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from backend.document_processor import extract_text

model = SentenceTransformer("all-MiniLM-L6-v2")

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

def build_knowledge_base(doc_path, index_path="models/faiss_index", data_path="models/docs.pkl"):
    with open(doc_path, "rb") as f:
        text = extract_text(f)
    chunks = split_text(text)
    embeddings = model.encode(chunks)

    # Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and chunks
    os.makedirs("models", exist_ok=True)
    faiss.write_index(index, index_path)
    with open(data_path, "wb") as f:
        pickle.dump(chunks, f)

    print("[INFO] Knowledge base built successfully.")
