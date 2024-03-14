from init import preprocessing_pipeline, indexing_pipeline
from typing import List
from haystack import Document
import textract

known_documents = set()

def add_documents(paths: List[str]):

    try:

        documents = []
        pdf_files = []
        doc_files = []

        for path in paths:
            if path.endswith('.pdf') or path.endswith('.txt') or path.endswith('.md'):
                if path not in known_documents:
                    pdf_files.append(path)
            elif path.endswith('.docx') or path.endswith('.doc'):
                if path not in known_documents:
                    doc_files.append(path)

        print(len(pdf_files), len(doc_files))

        if len(pdf_files)!=0:

            # Обрабатываем pdf, txt и md файлы
            processed_pdf_files = preprocessing_pipeline.run(
                {
                    "file_type_router": {
                        "sources": pdf_files
                    }
                }
            )

            processed_pdf_files = processed_pdf_files['document_joiner']['documents']
            for i in range(len(pdf_files)):
                processed_pdf_files[i].meta['title'] = pdf_files[i].split('/')[-1]
                processed_pdf_files[i].meta['url'] = pdf_files[i].split('/')[-1]


            known_documents.update(pdf_files)
            documents.extend(processed_pdf_files)

        if len(doc_files)!=0:

            # Обрабатываем DOC и DOCX файлы
            for file_path in doc_files:
                text = textract.process(file_path).decode()
                documents.append(Document(content=text, meta={"title": file_path.split('/')[-1], 'url': file_path.split('/')[-1]}))
                known_documents.add(file_path)

        print(documents)

        indexing_pipeline.run({"document_cleaner": {"documents": documents}})
    except Exception as e:
        print(e)
        return False
    
    return True