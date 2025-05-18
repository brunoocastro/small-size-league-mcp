# ENUM for filters
from enum import Enum
from logging import getLogger

from modules.db_management import VectorStoreManager

logger = getLogger(__name__)


class SSLSearchCategories(Enum):
    WEBSITE = "website"
    RULES = "rules"


vector_store_manager = VectorStoreManager()


# @lru_cache(maxsize=1)
def ssl_search_tool(
    query: str,
    k: int = 2,
    filter_source: SSLSearchCategories | None = None,
):
    """
    Retrieve the RoboCUP Small Size League (SSL) K most relevant documents based on a input query.
    These documents are relative from RoboCUP SSL website and rules.

    TIPS:
    - Provide the filter to retrieve documents from a specific source, if not provided, the tool will retrieve documents from all sources.
    - To get relevant documents, provide a query related to the RoboCUP SSL information.

    """
    # Args:
    #     query (str): The query to retrieve the most relevant documents from the RoboCUP SSL website, rules, and repository.
    #     k (int): The number of documents to retrieve.
    #     filter_source (str | None): The filter to apply to the documents.
    #         - "website": Only retrieve documents from the RoboCUP SSL website.
    #         - "rules": Only retrieve documents from the RoboCUP SSL rules.

    # Returns:
    #     List[Document]: A list of documents that are the most relevant to the query.

    vector_store = vector_store_manager.get()

    print(f"Filter: {filter_source}")
    print(f"Query: {query}")
    print(f"K: {k}")

    documents = vector_store.similarity_search_with_relevance_scores(
        query, k, {"score_threshold": 0.5, "filter": filter_source}
    )

    logger.info(f"Retrieved {len(documents)} documents for query: {query}")

    return documents
