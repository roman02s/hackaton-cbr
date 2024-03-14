from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors.document_splitter import DocumentSplitter
from haystack.components.preprocessors.document_cleaner import DocumentCleaner
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.converters import PyPDFToDocument, TextFileToDocument  # , MarkdownToDocument
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.rankers import TransformersSimilarityRanker, LostInTheMiddleRanker
# from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
# from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever

from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchBM25Retriever
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever
from elasticsearch import Elasticsearch

from haystack import Pipeline, Document
from haystack.utils import ComponentDevice

import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import glob
import os

import warnings
warnings.filterwarnings("ignore")

embedding_device = "cuda:3"
llm_device = "cuda:5"

def get_json_docs(path="../data"):
    """
    Extract documents from JSON files in a specified directory. Returns list of Documents.

    Args:
        path (str): path to JSON files

    Returns:
        List[Documents]: List with Documents contains content and meta data like title and url
    """
    docs = []
    json_files = glob.glob(f"{path}/*.json")
    for file_path in json_files:
        with open(file_path) as f:
            files = json.load(f)
        for file in files:
            docs.append(Document(content=file["text"], meta={"title": file["title"], "url": file["url"]}))
    return docs

# init preprocessing pipeline
# Компонеты для преобразования файлов pdf, txt и markdown в Documents
file_type_router = FileTypeRouter(mime_types=["text/plain", "application/pdf"])  # , "text/markdown"
text_file_converter = TextFileToDocument()
# markdown_converter = MarkdownToDocument()
pdf_converter = PyPDFToDocument()
document_joiner = DocumentJoiner()

# Добавление компонентов в пайплайн
preprocessing_pipeline = Pipeline()
preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
# preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")

# Маршрутизация пайплайна
preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
# preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")
preprocessing_pipeline.connect("text_file_converter", "document_joiner")
preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
# preprocessing_pipeline.connect("markdown_converter", "document_joiner")

# Init indexing pipeline
# хранилище документов с эмбеддингами
# document_store = InMemoryDocumentStore()

# os.environ["PG_CONN_STR"] = "postgresql://postgres:postgres@77.234.216.102:35432/postgres"

# document_store = PgvectorDocumentStore(
#     table_name="haystack_docs",
#     embedding_dimension=1024,
#     vector_function="cosine_similarity",
#     recreate_table=False,
#     search_strategy="hnsw",
# )

document_store = ElasticsearchDocumentStore(hosts= "http://77.234.216.102:9200/")

# шаг в пайплайне для очистки данных
document_cleaner = DocumentCleaner(
    remove_empty_lines=True,
    remove_extra_whitespaces=True,
    remove_repeated_substrings=False
)

# шаг для разбиения документов на более мелкие 
document_splitter = DocumentSplitter(split_by="word", split_length=300, split_overlap=10)

# модель для эмбеддингов. также здесь задается расчёт эмбеддингов для метаданных 
document_embedder = SentenceTransformersDocumentEmbedder(
    model="intfloat/multilingual-e5-large",
    meta_fields_to_embed=["title"], 
    device=ComponentDevice.from_str(embedding_device)
)

# шаг, который загружает документы в хранилище
document_writer = DocumentWriter(document_store, policy = DuplicatePolicy.SKIP)

# сборка пайплайна для генерации эмбеддингов и записи в хранилище
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("document_cleaner", document_cleaner)
indexing_pipeline.add_component("document_splitter", document_splitter)
indexing_pipeline.add_component("document_embedder", document_embedder)
indexing_pipeline.add_component("document_writer", document_writer)

indexing_pipeline.connect("document_cleaner", "document_splitter")
indexing_pipeline.connect("document_splitter", "document_embedder")
indexing_pipeline.connect("document_embedder", "document_writer")

# init_retrieval_pipeline
# модель для генерации эмбеддингов входного запроса
text_embedder = SentenceTransformersTextEmbedder(
    model="intfloat/multilingual-e5-large",
    device=ComponentDevice.from_str(embedding_device)
)

# инициализация эмбеддингового ретривера
embedding_retriever = ElasticsearchEmbeddingRetriever(document_store=document_store) # PgvectorEmbeddingRetriever(document_store=document_store)  # InMemoryEmbeddingRetriever(document_store)
# инициализация ретривера поиска по ключевым словам
# bm25_retriever = InMemoryBM25Retriever(document_store)
bm25_retriever = ElasticsearchBM25Retriever(document_store=document_store)

# шаг для конкатенации документов в один список
document_joiner = DocumentJoiner(join_mode='reciprocal_rank_fusion', top_k=5)

# ранкер, который сортирует документы так, чтобы наиболее релевантные находились сверху и снизу
# это помогает модели не терять контекст с высокой релевантностью
lost_in_the_middle_ranker = LostInTheMiddleRanker(word_count_threshold=1000, top_k=5)

# сборка пайплайна для инференса
retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component("text_embedder", text_embedder)
retrieval_pipeline.add_component("embedding_retriever", embedding_retriever)
retrieval_pipeline.add_component("bm25_retriever", bm25_retriever)
retrieval_pipeline.add_component("document_joiner", document_joiner)
retrieval_pipeline.add_component("lost_in_the_middle_ranker", lost_in_the_middle_ranker)

retrieval_pipeline.connect("text_embedder", "embedding_retriever")
retrieval_pipeline.connect("bm25_retriever", "document_joiner")
retrieval_pipeline.connect("embedding_retriever", "document_joiner")
retrieval_pipeline.connect("document_joiner", "lost_in_the_middle_ranker")
    
# Процессинг спаршенных данных
# json_docs = get_json_docs(path="../data")
# indexing_pipeline.run({"document_cleaner": {"documents": json_docs}})

# Загрузка модели и её квантизация
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map=llm_device, quantization_config=bnb_config)
