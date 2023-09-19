from dotenv import dotenv_values
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings


API_KEY = dotenv_values(".env").get("OPEN_AI_KEY")

loader = DirectoryLoader('./corpus/Mahabharata', glob="**/*.txt", loader_cls=TextLoader)
docs = loader.load()
textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
splitDocs = textSplitter.split_documents(docs)
client = chromadb.PersistentClient(path="./db")
db = Chroma.from_documents(splitDocs, OpenAIEmbeddings(openai_api_key=API_KEY), client=client)
