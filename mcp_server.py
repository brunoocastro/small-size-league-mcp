import logging
from enum import Enum
from functools import lru_cache

from fastmcp import FastMCP

import config
from db_management import VectorStoreManager

logger = logging.getLogger(__name__)


# Create MCP server
server = FastMCP("small-size-league-mcp")


# ENUM for filters
class Filter(Enum):
    WEBSITE = "website"
    RULES = "rules"
    REPOSITORY = "repository"


@server.tool()
async def retrieve_k_relevant_documents(
    query: str,
    k: int = 2,
    filter: Filter | None = None,
):
    """
    Retrieve the K most relevant documents based on the query related to the RoboCUP Small Size League (SSL) information.
    These documents are relative from RoboCUP SSL website, rules, and repository.
    Provide the filter to retrieve documents from a specific source, if not provided, the tool will retrieve documents from all sources.
    The tool will return a list of documents that are the most relevant to the query.
    The documents are sorted by relevance to the query.

    To get relevant documents, provide a query related to the RoboCUP SSL information.

    Args:
        query (str): The query to retrieve the most relevant documents from the RoboCUP SSL website, rules, and repository.
        k (int): The number of documents to retrieve.
        filter (str | None): The filter to apply to the documents.
            - "website": Only retrieve documents from the RoboCUP SSL website.
            - "rules": Only retrieve documents from the RoboCUP SSL rules.
            - "repository": Only retrieve documents from the RoboCUP SSL repository.

    Returns:
        List[Document]: A list of documents that are the most relevant to the query.
    """

    vector_store_manager = VectorStoreManager()
    vector_store = vector_store_manager.get()

    print(f"Filter: {filter}")

    documents = vector_store.similarity_search(query, k, filter)

    logger.info(f"Retrieved {len(documents)} documents for query: {query}")

    return documents


@lru_cache(maxsize=128)
@server.resource("full-text://urls")
async def get_website_urls():
    """
    Retrieve the full list of website URLs.
    This function reads URLs from a file specified in the configuration.
    The file is expected to contain one URL per line.
    """
    with open(config.URLS_FILE_PATH, "r") as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
    logger.info(f"Retrieved {len(urls)} URLs from file: {config.URLS_FILE_PATH}")
    return urls


@lru_cache(maxsize=128)
@server.resource("full-text://website")
async def get_full_website_text():
    """
    Retrieve the full text of the RoboCUP SSL website.
    This function reads the full text from a file specified in the configuration.
    The file is expected to contain the complete text of the website.
    """
    with open(config.FULL_WEBSITE_FILE_PATH, "r") as file:
        full_website_text = file.read()

    logger.info(
        f"Retrieved full website text from file: {config.FULL_WEBSITE_FILE_PATH}"
    )
    logger.info(f"Full website text length: {len(full_website_text)} characters")
    logger.info(f"Full website text preview: {full_website_text[:100]}")
    # Ensure the text is not empty
    if not full_website_text:
        logger.warning("Full website text is empty.")
        return "No website text found. The tool didn't find any website text."

    # Return the full website text
    logger.info(f"Full website text length: {len(full_website_text)} characters")
    return full_website_text


@lru_cache(maxsize=128)
@server.resource("full-text://rules")
async def get_full_rules_text():
    """
    Retrieve the full text of the RoboCUP SSL rules.
    This function reads the full text from a file specified in the configuration.

    Returns:
        str: The full text of the RoboCUP SSL rules.
    """
    with open(config.FULL_RULES_FILE_PATH, "r") as file:
        full_rules_text = file.read()

    if not full_rules_text:
        logger.warning("Full rules text is empty.")
        return "No rules text found. The tool didn't find any rules text."

    return full_rules_text


@lru_cache(maxsize=128)
@server.resource("full-text://repository")
async def get_full_repository_text():
    """
    Retrieve the full text of the RoboCUP SSL repository.
    This function reads the full text from a file specified in the configuration.
    """
    with open(config.FULL_REPOSITORY_FILE_PATH, "r") as file:
        full_repository_text = file.read()

    if not full_repository_text:
        logger.warning("Full repository text is empty.")
        return "No repository text found. The tool didn't find any repository text."

    return full_repository_text


if __name__ == "__main__":
    server.run(transport="sse", log_level="debug")
