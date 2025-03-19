from langchain_core.prompts import ChatPromptTemplate

class Adapter:
    def __init__(self, env):
        self.llm_text = env("LLM_TYPE")
        self.role = env("LLM_ROLE", default="You are a story teller")
        self.prompt = ChatPromptTemplate([
            ("system", self.role),
            ("human", "chat_history:{chat_history}\n{query}"),
        ])
        if self.llm_text.lower() == "openai":
            # from langchain_openai import OpenAIEmbeddings
            from langchain_openai import ChatOpenAI
            self.llm_chat = ChatOpenAI(
                temperature=env.float("OPENAI_TEMP", default=0.5), model=env("OPENAI_MODEL"), openai_api_key=env("OPENAI_API_KEY")
            )
            # self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        elif self.llm_text.lower() == "local":
            # from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_ollama import ChatOllama
            self.llm_chat = ChatOllama(
                base_url=env("OLLAMA_ENDPOINT", default="127.0.0.1"), model=env("OLLAMA_MODEL"), num_ctx=env.int("OLLAMA_TOKENS", default=2048), temperature=env.float("OLLAMA_TEMP", default=0.5)
            )
            # model_name = "BAAI/bge-small-en"
            # model_kwargs = {"device": "cpu"}
            # encode_kwargs = {"normalize_embeddings": True}
            # self.embedding = HuggingFaceEmbeddings(
            #     model_name=model_name,
            #     model_kwargs=model_kwargs,
            #     encode_kwargs=encode_kwargs,
            # )
        elif self.llm_text.lower() == "hybrid":
            from langchain_openai import OpenAIEmbeddings, OpenAI
            # from langchain_huggingface import HuggingFaceEmbeddings

            self.llm = OpenAI(temperature=0, openai_api_key=env("OPENAI_API_KEY"))
            # model_name = "BAAI/bge-small-en"
            # model_kwargs = {"device": "cpu"}
            # encode_kwargs = {"normalize_embeddings": True}
            # self.embedding = HuggingFaceEmbeddings(
            #     model_name=model_name,
            #     model_kwargs=model_kwargs,
            #     encode_kwargs=encode_kwargs,
            # )
        else:
            raise ValueError("Invalid LLM: Please set LLM_TYPE to either 'openai' or 'local'")

    def chat(self, query, chat_history):
        from langchain_core.output_parsers import StrOutputParser
        chain =  self.prompt | self.llm_chat | StrOutputParser()
        result = chain.invoke({"query":query, "chat_history":chat_history})
        return result

    