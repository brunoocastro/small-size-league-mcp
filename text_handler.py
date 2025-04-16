import hashlib
import re
import uuid
from typing import List, Tuple

import tiktoken
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

from config import FULL_WEBSITE_FILE_PATH


def count_tokens(text, model="cl100k_base"):
    """
    Count the number of tokens in the text using tiktoken.

    Args:
        text (str): The text to count tokens for
        model (str): The tokenizer model to use (default: cl100k_base for GPT-4)

    Returns:
        int: Number of tokens in the text
    """
    encoder = tiktoken.get_encoding(model)
    return len(encoder.encode(text))


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Target the main article content for documentation
    main_content = soup.find("article", class_="status-publish")

    # If found, use that, otherwise fall back to the whole document
    content = main_content.get_text() if main_content else soup.text

    # Clean up whitespace
    content = re.sub(r"\n\n+", "\n\n", content).strip()

    return content


def load_site(urls: List[str]) -> Tuple[List[Document], List[int]]:
    """
    Load information from the official website.

    This function:
    1. Uses RecursiveUrlLoader to fetch pages from the website
    2. Counts the total documents and tokens loaded

    Returns:
        list: A list of Document objects containing the loaded content
        list: A list of tokens per document
    """
    print("Loading website...")

    docs = []
    # Show the progress
    for url in tqdm(
        urls,
        desc="Processing URLs and loading page content",
        total=len(urls),
        unit="URLs",
    ):
        loader = RecursiveUrlLoader(
            url,
            max_depth=3,
            extractor=bs4_extractor,
        )

        # Load documents using lazy loading (memory efficient)
        docs_lazy = loader.lazy_load()

        # Load documents and track URLs
        for d in docs_lazy:
            d.metadata["source"] = url
            docs.append(d)

    print(f"Loaded {len(docs)} documents from website.")

    # Count total tokens in documents
    total_tokens = 0
    tokens_per_doc = []
    for doc in tqdm(
        docs, desc="Counting tokens in documents", total=len(docs), unit="documents"
    ):
        total_tokens += count_tokens(doc.page_content)
        tokens_per_doc.append(count_tokens(doc.page_content))

    print(f"Total tokens in loaded documents: {total_tokens}")

    return docs, tokens_per_doc


def save_full_website(
    documents: List[Document], full_website_file_path: str = FULL_WEBSITE_FILE_PATH
):
    """Save the documents to a file"""

    # Open the output file
    with open(full_website_file_path, "w") as f:
        # Write each document
        for i, doc in enumerate(documents):
            # Get the source (URL) from metadata
            source = doc.metadata.get("source", "Unknown URL")

            # Write the document with proper formatting
            f.write(f"DOCUMENT {i + 1}\n")
            f.write(f"SOURCE: {source}\n")
            f.write("CONTENT:\n")
            f.write(doc.page_content)
            f.write("\n\n" + "=" * 80 + "\n\n")

    print(f"Documents concatenated into {full_website_file_path}")


def split_documents(documents: List[Document]):
    """
    Split documents into smaller chunks for improved retrieval.

    This function:
    1. Uses RecursiveCharacterTextSplitter with tiktoken to create semantically meaningful chunks
    2. Ensures chunks are appropriately sized for embedding and retrieval
    3. Counts the resulting chunks and their total tokens

    Args:
        documents (list): List of Document objects to split

    Returns:
        list: A list of split Document objects
    """
    print("Splitting documents...")

    # Initialize text splitter using tiktoken for accurate token counting
    # chunk_size=8,000 creates relatively large chunks for comprehensive context
    # chunk_overlap=500 ensures continuity between chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=8000, chunk_overlap=500
    )

    # Split documents into chunks
    split_docs = text_splitter.split_documents(documents)

    print(f"Created {len(split_docs)} chunks from documents.")

    # Generate a deterministic ID based on the URL
    for doc in split_docs:
        source = doc.metadata["source"] or uuid.uuid4()
        content = doc.page_content or uuid.uuid4()
        # Create a unique hash string using the source and content
        # This ensures that the same content always generates the same ID
        # This is important for reproducibility and consistency
        # and to avoid collisions in the database
        hash_string = f"{source}-{content}"

        # Generate a deterministic ID based on the URL and content
        url_hash = hashlib.md5(hash_string.encode()).hexdigest()
        doc.metadata["id"] = f"doc_{url_hash}"

    # Count total tokens in split documents
    total_tokens = 0
    for doc in split_docs:
        total_tokens += count_tokens(doc.page_content)

    print(f"Total tokens in split documents: {total_tokens}")

    return split_docs
