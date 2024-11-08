import os

from langchain_openai import AzureOpenAIEmbeddings
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch

from pymongo import MongoClient


def format_docs(docs):
    """Combine relevant documents into a context"""
    return "\n\n".join(doc.page_content for doc in docs)


mongodb_user = os.environ.get("MONGODB_USER")
mongodb_password = os.environ.get("MONGODB_PASSWORD")
mongodb_cluster = os.environ.get("MONGODB_CLUSTER")

MONGODB_CLUSTER_URI = (
    f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_cluster}"
)

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    chunk_size=16
)

client = MongoClient(MONGODB_CLUSTER_URI)

DB_NAME = os.environ.get("DB_NAME")
VECTOR_COLLECTION = os.environ.get("VECTOR_COLLECTION")
VECTOR_SEARCH_INDEX = os.environ.get("VECTOR_SEARCH_INDEX")

MONGODB_COLLECTION = client[DB_NAME][VECTOR_COLLECTION]

vectorstore = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=VECTOR_SEARCH_INDEX,
    relevance_score_fn="cosine",
)
