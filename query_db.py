import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from story_query import StoryQuery

import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

API_KEY = st.secrets["OPEN_AI_KEY"]






def build_story(query):
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

    storied_query = StoryQuery(query=query).transform_prompt()

    logging.info("Storied query: {storied_query}")
    
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(search_kwargs={'k': 1}), llm=llm,
    )

    QA_CHAIN_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Moreover, try to make the context into a full story with vivid narration and descriptions.
    The context will also have a title, make sure to include it. 
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

    logging.info(result["source_documents"])

    return result["result"]