# --- backend/knowledge_base_builder.py ---
import os
import faiss
from sentence_transformers import SentenceTransformer
from backend.document_processor import extract_text

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = []

for file in os.listdir("data"):
    with open(os.path.join("data", file), 'r', encoding='utf-8', errors='ignore') as f:
        texts.append(f.read())

chunks = [t[i:i+500] for t in texts for i in range(0, len(t), 500)]
embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

if not os.path.exists("models"):
    os.makedirs("models")
faiss.write_index(index, "models/faiss_index")

with open("models/chunks.txt", "w", encoding='utf-8') as f:
    for c in chunks:
        f.write(c + "\n")