# --- backend/chatbot_engine.py ---
import faiss
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama

model = SentenceTransformer("all-MiniLM-L6-v2")
llm = Ollama(model="llama3:8b")
index = faiss.read_index("models/faiss_index")

with open("models/chunks.txt", "r", encoding='utf-8') as f:
    chunks = f.readlines()

def query_knowledge_base(query):
    query_vector = model.encode([query])
    D, I = index.search(query_vector, k=3)
    context = "\n".join([chunks[i] for i in I[0]])
    prompt = f"Use the context to answer: {query}\n\nContext:\n{context}"
    return llm.invoke(prompt)