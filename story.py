from json import JSONEncoder
import json
import logging

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from dotenv import dotenv_values
from story_query import StoryQuery




API_KEY = dotenv_values(".env").get("OPEN_AI_API_KEY")


logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

"""Classes to represent and build a story"""


class PageContent:
    """
    Encapsulates the content of a page
    """
    def __init__(self, text):
        self.text = text

class Page(JSONEncoder):
    """Represents a page"""
    def __init__(self, content:PageContent, pageNo):
        self.content = content
        self.pageNo = pageNo

    def default(self, o):
        return o.__dict__

class Katha:
    """
    Represents a story
    """
    def __init__(self, query):


        self.query = query

        self.story_text = None

        self.pages = []

        
   
    def build_story(self):
        """
        Pipeline for building a story:

        1. Transform query into a StoryQuery
        2. Run a MultiQuery retriever that fetches relevant documents
        from vector datastore based on multiple queries similar to the storied query
        3. Pass in the most relevant document as context to LLM and answer the storied query.
        """
        
        vectordb = Chroma(persist_directory="./db",
                    embedding_function=OpenAIEmbeddings(openai_api_key=API_KEY)
        )

        llm = ChatOpenAI(temperature=0.0, openai_api_key=API_KEY)

        storied_query = StoryQuery(query=self.query).transform_prompt()

        logging.info("Storied query: {storied_query}")
        
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=vectordb.as_retriever(search_kwargs={'k': 1}), llm=llm,
        )

        QA_CHAIN_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Moreover, try to make the context into a full story with vivid narration and descriptions.
        Write from the point of view of a grandparent telling their grandchild a story.
        Separate new paragraphs with two new lines.
        {context}
        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(QA_CHAIN_TEMPLATE)

        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever_from_llm,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True
        )
        
        
        result = qa_chain({"query":storied_query})

        logging.info(result)

        self.story_text = result["result"]

    
    def build_pages(self):
        """
        Populates self.pages
        """
        splitter ='\n\n'
        self.pages = [
            Page(
                content=page,
                pageNo=(i+1)
            ) for (i, page) in enumerate(
                list(
                    filter(lambda x:x and x!=" ",
                        self.story_text.split(splitter))
                    )
                )
        ]




            



        