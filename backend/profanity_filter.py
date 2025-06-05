# backend/profanity_filter.py

def load_bad_words(filepath="assets/bad_words.txt"):
    with open(filepath, "r") as file:
        return set(line.strip().lower() for line in file)

BAD_WORDS = load_bad_words()

def contains_profanity(text):
    words = text.lower().split()
    return any(word in BAD_WORDS for word in words)
