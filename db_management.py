import logging
from functools import lru_cache
from typing import List

from langchain_chroma.vectorstores import Chroma
from langchain_core.documents import Document

from config import DATA_PATH, VECTOR_STORE_COLLECTION_NAME
from providers import embedding_provider

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
class VectorStoreManager:
    def __init__(
        self,
        persist_path: str = DATA_PATH,
        collection_name: str = VECTOR_STORE_COLLECTION_NAME,
    ):
        self.vector_store_instance = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_provider,
            persist_directory=persist_path,
        )

    def add_or_update_documents(self, documents: List[Document]):
        ids = [str(d.metadata["id"]) for d in documents]

        print("documents", documents)

        logger.info(f"Adding {len(documents)} new documents")

        # Deduplicate documents
        documents, ids = self.deduplicate_documents(documents, ids)

        # Add new documents
        self.vector_store_instance.add_documents(documents=documents, ids=ids)
        logger.info(f"Added {len(documents)} new documents")

    @staticmethod
    def deduplicate_documents(documents, ids):
        seen = set()
        unique_docs = []
        unique_ids = []
        for doc, id_ in zip(documents, ids):
            if id_ not in seen:
                unique_docs.append(doc)
                unique_ids.append(id_)
                seen.add(id_)
        return unique_docs, unique_ids

    def get(self) -> Chroma:
        return self.vector_store_instance
