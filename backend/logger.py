# --- backend/logger.py ---
def log_chat(email, query, response):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{email} | Q: {query} | A: {response}\n")