from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import chromadb

API_KEY = st.secrets("OPEN_AI_KEY")
vectordb = Chroma(persist_directory="./db", embedding_function=OpenAIEmbeddings(openai_api_key=API_KEY))

def getMostRelevantStory(query):
    return vectordb.similarity_search(query)[0].page_content

