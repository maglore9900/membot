from langchain_core.prompts import ChatPromptTemplate
from modules import prompts


class Adapter:
    def __init__(self, env):
        self.llm_text = env("LLM_TYPE")
        self.prompt = ChatPromptTemplate.from_template(prompts.main)
        if self.llm_text.lower() == "openai":
            from langchain_openai import OpenAIEmbeddings
            from langchain_openai import ChatOpenAI
            self.llm_chat = ChatOpenAI(
                temperature=0.3, model=env("OPENAI_MODEL"), openai_api_key=env("OPENAI_API_KEY")
            )
            self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        elif self.llm_text.lower() == "local":
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_ollama import ChatOllama
            self.llm_chat = ChatOllama(
                base_url=env("OLLAMA_ENDPOINT"), model=env("OLLAMA_MODEL")
            )
            model_name = "BAAI/bge-small-en"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            self.embedding = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )
        elif self.llm_text.lower() == "hybrid":
            from langchain_openai import OpenAIEmbeddings, OpenAI
            from langchain_huggingface import HuggingFaceEmbeddings

            self.llm = OpenAI(temperature=0, openai_api_key=env("OPENAI_API_KEY"))
            model_name = "BAAI/bge-small-en"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            self.embedding = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )
        else:
            raise ValueError("Invalid LLM")

    def chat(self, query, chat_history):
        from langchain_core.output_parsers import StrOutputParser
        chain = self.prompt | self.llm_chat | StrOutputParser()
        result = chain.invoke({"query":query, "chat_history":chat_history})
        return result

    