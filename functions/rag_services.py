from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from functions.example_documents import documents


def format_docs(docs):
    """Combine relevant documents into a context"""
    return "\n\n".join(doc.page_content for doc in docs)


embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    chunk_size=16
)

vectorstore = InMemoryVectorStore.from_documents(
    documents=documents, embedding=embeddings
)
