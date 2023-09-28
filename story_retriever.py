from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
from story_query import StoryQuery


class StoryRetriever:
    """
    Class that retrieves most relevant document to a query, after applying a transformation to it.
    """
    API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")
    def __init__(self, query):
        self.query = query
        self.storied_query = StoryQuery(query).transform_prompt()
        self.llm = ChatOpenAI(temperature=0.0, openai_api_key = StoryRetriever.API_KEY)

    def retrieve(self):
        """
        Returns most relevant document to [storiedQuery]
        """
        vectordb = Chroma(persist_directory="./db",embedding_function=OpenAIEmbeddings(openai_api_key=StoryRetriever.API_KEY))
        retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={'k': 1}), llm=self.llm)
        return retriever_from_llm.get_relevant_documents(query=self.storied_query)[0].page_content




