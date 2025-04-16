import logging
from typing import List

from langchain_chroma.vectorstores import Chroma
from langchain_core.documents import Document

from config import VECTOR_STORE_COLLECTION_NAME, VECTOR_STORE_PATH
from providers import embedding_provider

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_path: str = VECTOR_STORE_PATH, collection_name: str = VECTOR_STORE_COLLECTION_NAME):
        self.vector_store_instance = Chroma(
            collection_name=collection_name,        
            embedding_function=embedding_provider,
            persist_directory=persist_path,
        )

    def add_or_update_documents(self, documents: List[Document]):
        ids = [str(d.metadata["id"]) for d in documents]

        logger.info(f"Adding {len(documents)} new documents")

        # Add new documents
        self.vector_store_instance.add_documents(documents=documents, ids=ids)
        logger.info(f"Added {len(documents)} new documents")
    def get(self):
        return self.vector_store_instance
