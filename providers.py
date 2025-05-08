# Here we define the providers used in the project
# from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm_chat_provider = ChatOpenAI(model="gpt-4o-mini")

embedding_provider = OpenAIEmbeddings(model="text-embedding-3-small")
