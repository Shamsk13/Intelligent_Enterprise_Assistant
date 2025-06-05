# backend/logger.py

import os
from datetime import datetime

CHAT_LOG_FILE = "logs/chat_log.txt"
DOC_LOG_FILE = "logs/document_log.txt"

def log_chat(email, user_msg, bot_msg):
    with open(CHAT_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {email} | USER: {user_msg} | BOT: {bot_msg}\n")

def log_document(email, filename):
    with open(DOC_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {email} uploaded {filename}\n")
