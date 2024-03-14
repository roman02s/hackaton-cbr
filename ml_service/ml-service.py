from fastapi import FastAPI, HTTPException
from haystack import Document
from pydantic import BaseModel
from typing import List
from init import indexing_pipeline, retrieval_pipeline, model, tokenizer, embedding_device, llm_device
import os

from preprocessing import add_documents

app = FastAPI()

class TextItem(BaseModel):
    text: str

class TextList(BaseModel):
    texts: List[str]

@app.post("/load_text/")
async def load_text(query: TextItem):
    """
    Эндпоинт для загрузки своего текста в векторную БД

    Args:
        path (TextItem): текст для добавления в векторную БД

    Returns:
        bool: флаг, что загрузка прошла успешно
    """
    try:
        doc = Document(content=query.text, meta={"title": 'Custom data'})
        indexing_pipeline.run({"document_cleaner": {"documents": [doc]}})
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/drag_n_drop/")
async def drag_n_drop(query: TextList):
    """
    Эндпоинт для загрузки документов в векторную БД через drag n drop

    Args:
        path (TextList): список путей до сохраненных файлов (.pdf, .docx, ...)

    Returns:
        bool: флаг, что загрузка прошла успешно
    """
    try:
        docs_paths = []
        return_value = True
        for fname in query.texts:
            if os.path.isfile(fname):
                docs_paths.append(fname)
            else:
                return_value = False
        
        value = add_documents(docs_paths)
        return_value = return_value and value
        return return_value
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/")
async def query_text(query: TextItem):
    """
    Эндпоинт для обработки входящих запросов

    Args:
        query (TextItem): текстовый запрос

    Returns:
        str: строка с ответом модели
    """
    try:
        query = query.text
        result = retrieval_pipeline.run(
            {"text_embedder": {"text": query}, "bm25_retriever": {"query": query}}
        )
        help_information = ''
        sources = []
        for doc in result["lost_in_the_middle_ranker"]["documents"]:
            doc.meta["title"] = doc.meta.get('title', 'NaN')
            doc.meta["url"] = doc.meta.get('url', 'NaN')
            # doc.meta["score"] = doc.meta.get('score', 'NaN')
            source = {'title': doc.meta["title"], 'url': doc.meta["url"], 'score': doc.score}
            sources.append(source)
            source_str = doc.meta["title"] + ", URL: " + doc.meta["url"] + ", Score: " + str(doc.score)
            help_information+="Источник: " + source_str  + '\n'
            help_information+="Текст: " + doc.content+'\n'

        messages = [
            {"role": "user", "content": f"Ответь на вопрос: {query} \n Используй вспомогательную информацию: {help_information} \nОтвечай на русском"},
        ]
        
        input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt").to(llm_device) # cuda
        
        outputs = model.generate(input_ids, max_new_tokens=500)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = '\n  Ответ:  \n' + answer[answer.find('[/INST]') + len('[/INST] '):]
        response += '\n  Источники ответа:'
        sources_url_set = set()
        for source in sources:
            if source['score'] > 0.7 and source['url'] not in sources_url_set:
                sources_url_set.add(source['url'])
                response += f"\n  Заголовок: {source.get('title', 'NaN')}, URL: {source.get('url', 'NaN')}, Score: {source.get('score', 'NaN')}"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
