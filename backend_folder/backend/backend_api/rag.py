from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os

"""model = OllamaLLM(model="llama3.1")

system_message = "You are an interactive QA system that provides accurate responses.You are also helpful and love using emojis to be more interactive."

prompt = ChatPromptTemplate.from_template(system_message)"""

def ingest():
    dir_path = file_path = os.path.dirname(os.path.abspath(__file__)) + "/documents"

    loader = DirectoryLoader(dir_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # create embeddings and store the vectors in a chroma_db
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
    db.persist()
