from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

model = OllamaLLM(model="llama3.1")

system_prompt = """
You are an interactive QA system that provides accurate responses.
You are also helpful and love using emojis to be more interactive.
Context:
{context}

Chat history:
{chat_history}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(system_prompt)

# load docs
loader = DirectoryLoader("docs/", glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# create embeddings and store the vectors in a chroma_db
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
retreiver = db.as_retriever()

# handle memory for conversation
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# conversational retreival chain
qa = ConversationalRetrievalChain.from_llm(
    llm=model,
    retriever=retreiver,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)

print("Chatbot ready! Type 'exit' to quit.\n")
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break
    result = qa.invoke(query)
    print("Bot:", result)

print("MEMORY RECORDED:: ")
print(memory.chat_memory)