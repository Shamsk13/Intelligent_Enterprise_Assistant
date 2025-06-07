# backend/knowledge_base_builder.py

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.document_processor import extract_text

print("✅ Script started")

model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def build_knowledge_base(data_folder="data", index_path="models/faiss_index", data_path="models/docs.pkl"):
    print("🚀 build_knowledge_base called")

    all_chunks = []

    if not os.path.exists(data_folder):
        print(f"[ERROR] Data folder '{data_folder}' does not exist.")
        return

    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        if filename.endswith((".pdf", ".docx")):
            try:
                print(f"[INFO] Processing {filename}")
                text = extract_text(filepath)
                if not text.strip():
                    print(f"[WARNING] No text found in {filename}")
                    continue
                chunks = split_text(text)
                all_chunks.extend(chunks)
                print(f"[INFO] Extracted {len(chunks)} chunks from {filename}")
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")
        else:
            print(f"[SKIPPED] {filename} is not a PDF or DOCX")

    if not all_chunks:
        print("[ERROR] No text chunks extracted.")
        return

    embeddings = model.encode(all_chunks, show_progress_bar=True)
    os.makedirs("models", exist_ok=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, index_path)

    with open(data_path, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"[✅ SUCCESS] Built knowledge base with {len(all_chunks)} chunks.")
    print(f"[📁] FAISS index saved to: {index_path}")
    print(f"[📁] Chunks saved to: {data_path}")

if __name__ == "__main__":
    print("📦 __main__ running")
    build_knowledge_base()
    