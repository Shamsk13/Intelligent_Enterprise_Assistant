# --- backend/profanity_filter.py ---
def contains_profanity(text):
    blacklist = ["badword1", "badword2"]
    return any(word in text.lower() for word in blacklist)