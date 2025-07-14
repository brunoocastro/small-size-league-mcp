# ENUM for filters
from enum import Enum
from logging import getLogger

from modules.db_management import VectorStoreManager

logger = getLogger(__name__)


class SSLDocumentSource(Enum):
    WEBSITE = "website_pages"
    RULES = "rules"


vector_store_manager = VectorStoreManager()


def ssl_search_tool(
    query: str,
    k: int = 2,
    document_source_filter: SSLDocumentSource | None = None,
    threshold: float = 0,
):
    """
    Retrieve the RoboCUP Small Size League (SSL) K most relevant documents based on a input query.
    These documents are relative from RoboCUP SSL website and rules.

    TIPS:
    - Provide the filter to retrieve documents from a specific source, if not provided, the tool will retrieve documents from all sources.
    - To get relevant documents, provide a query related to the RoboCUP SSL information.
    - If the threshold is set to 0, all documents will be returned.
    - If the threshold is set to a value greater than 0, only documents with a relevance score greater than or equal to the threshold will be returned.
    - If the results are too random, try to increase the threshold value.

    """
    vector_store = vector_store_manager.get()

    logger.info(
        f"Starting SSL search tool. Kwargs:\nQuery: {query}, k: {k}, document_source_filter: {document_source_filter}, threshold: {threshold}"
    )

    result = vector_store.similarity_search_with_relevance_scores(
        query,
        k=k,
        filter=(
            {"type": str(document_source_filter.value)}
            if document_source_filter
            else None
        ),
        score_threshold=threshold,
    )

    # Filter documents based on the threshold
    filtered_documents = [doc for doc, score in result if score >= threshold]

    if len(filtered_documents) == 0:
        logger.warning(
            f"No documents found.Filters:\n type={document_source_filter}, k={k} and threshold={threshold}. Original query: '{query}'"
        )
    else:
        logger.info(
            f"Retrieved {len(filtered_documents)} documents for query: '{query}'"
        )

    return filtered_documents
