from haystack import Document
import glob
import pdfplumber
import textract


def read_files(path):
    docs = []

    # Добавляем поиск файлов PDF и DOC/DOCX
    pdf_files = glob.glob("./data/*.pdf")
    doc_files = glob.glob("./data/*.doc") + glob.glob("./data/*.docx")

    # Обрабатываем PDF файлы
    for file_path in pdf_files:
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages if page.extract_text() is not None])
        docs.append(Document(content=text, meta={"filename": file_path}))

    # Обрабатываем DOC и DOCX файлы
    for file_path in doc_files:
        text = textract.process(file_path).decode()
        docs.append(Document(content=text, meta={"filename": file_path}))
    return docs
