#backend/chatbot_engine.py
import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

faiss_index_path = "models/faiss_index"
chunks_path = "models/docs.pkl"

try:
    index = faiss.read_index(faiss_index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    print("[INFO] Knowledge base loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load knowledge base: {e}")
    index = None
    chunks = []

def query_knowledge_base(user_query):
    if not index or not chunks:
        return "Knowledge base not available. Please try again later."

    query_embedding = model.encode([user_query])
    D, I = index.search(query_embedding, k=1)
    if I[0][0] < len(chunks):
        return chunks[I[0][0]]
    return "Sorry, I couldn't find anything relevant."



