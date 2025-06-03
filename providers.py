from settings import LLM_Providers, MCP_Settings

settings = MCP_Settings()

if settings.LLM_PROVIDER == LLM_Providers.OPENAI:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings

    llm_chat_provider = ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_HOST,
    )

    embedding_provider = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL, api_key=settings, base_url=settings.LLM_HOST
    )
else:
    from langchain_ollama import ChatOllama, OllamaEmbeddings

    llm_chat_provider = ChatOllama(model=settings.LLM_MODEL, host=settings.LLM_HOST)
    embedding_provider = OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL, host=settings.LLM_HOST
    )
