# Here we define the providers used in the project
from langchain_ollama import ChatOllama, OllamaEmbeddings

llm_chat_provider = ChatOllama(model="gemma3")

embedding_provider = OllamaEmbeddings(model="nomic-embed-text")