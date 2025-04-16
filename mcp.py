import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import lru_cache

from langchain_chroma import Chroma

import config
from db_management import VectorStoreManager
from mcp.server.fastmcp import Context, FastMCP

logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    """
    Context for the application. This can be used to store global variables or configurations.
    """

    vector_store: Chroma
    url_file: str
    full_website_file: str


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    vector_store_manager = VectorStoreManager()
    vector_store = vector_store_manager.get()

    base_path = os.getcwd()

    logger.info("Application startup: Vector store initialized.")

    # Load URL file and full website file
    try:
        full_url_path = os.path.join(base_path, config.URLS_FILE_PATH)
        with open(full_url_path, "r") as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls]
        logger.info(f"Loaded {len(urls)} URLs from file: {full_url_path}")
    except FileNotFoundError:
        logger.error(f"URL file not found: {full_url_path}")
        urls = []

    try:
        full_website_path = os.path.join(base_path, config.FULL_WEBSITE_FILE_PATH)
        with open(full_website_path, "r") as file:
            full_website_text = file.read()
        logger.info(f"Loaded full website text from file: {full_website_path}")
    except FileNotFoundError:
        logger.error(f"Full website file not found: {full_website_path}")
        full_website_text = ""

    yield AppContext(
        vector_store=vector_store,
        url_file="\n".join(urls),
        full_website_file=full_website_text,
    )


# Create MCP server
mcp = FastMCP("small-size-league-mcp", lifespan=app_lifespan)


@mcp.tool()
def retrieve_k_relevant_documents(
    query: str,
    ctx: Context,
    k: int = 3,
):
    """
    Retrieve the K most relevant documents based on the query related to the RoboCUP Small Size League (SSL) information.
    These documents are relative from RoboCUP SSL website
    """
    documents = ctx.request_context.lifespan_context.vector_store.similarity_search(
        query, k
    )

    logger.info(f"Retrieved {len(documents)} documents for query: {query}")

    return documents


@lru_cache(maxsize=128)
@mcp.resource("website://urls")
def get_website_urls():
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
@mcp.resource("website://full_text")
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
    # Ensure the text is not empty
    if not full_website_text:
        logger.warning("Full website text is empty.")
        return ""

    # Return the full website text
    logger.info(f"Full website text length: {len(full_website_text)} characters")
    return full_website_text


if __name__ == "__main__":
    mcp.run()
