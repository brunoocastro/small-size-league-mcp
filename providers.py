# Here we define the providers used in the project

from langchain_openai import ChatOpenAI

llm_chat_provider = ChatOpenAI(model="gpt-4o-mini")
