# --- backend/document_processor.py ---
def extract_text(file):
    import docx2txt, PyPDF2
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return file.read().decode("utf-8", errors="ignore")

def process_document(uploaded_file):
    text = extract_text(uploaded_file)
    path = os.path.join("data", uploaded_file.name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)