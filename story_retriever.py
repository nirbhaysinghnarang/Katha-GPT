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
    Class that retrieves the most relevant document to a query after applying a transformation to it.

    This class is designed to retrieve the most relevant document in response to a query. It transforms the query
    using the `StoryQuery` class, applies a transformation prompt, and retrieves the most relevant document
    using a vector store and a language model.

    Attributes:
        API_KEY (str): The OpenAI API key loaded from the .env file.
        query (str): The original query.
        storied_query (str): The transformed query with a prompt.
        llm (ChatOpenAI): The language model used for retrieval.

    Example usage:

    >>> from story_query import StoryQuery
    >>> query = "Tell me a story about adventure."
    >>> retriever = StoryRetriever(query)
    >>> relevant_document = retriever.retrieve()
    >>> print(relevant_document)
    """

    API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")

    def __init__(self, query):
        """
        Initialize a StoryRetriever instance.

        Args:
            query (str): The original query.
        """
        self.query = query
        self.storied_query = StoryQuery(query).transform_prompt()
        self.llm = ChatOpenAI(temperature=0.0, openai_api_key=StoryRetriever.API_KEY)

    def retrieve(self):
        """
        Retrieve the most relevant document in response to the transformed query.

        Returns:
            str: The content of the most relevant document.

        Example usage:

        >>> relevant_document = retriever.retrieve()
        >>> print(relevant_document)
        """
        vectordb = Chroma(persist_directory="./db", embedding_function=OpenAIEmbeddings(openai_api_key=StoryRetriever.API_KEY))
        retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={'k': 1}), llm=self.llm)
        return retriever_from_llm.get_relevant_documents(query=self.storied_query)[0].page_content
