from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
import json
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

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

chat_messages = []

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = db.as_retriever()

qa = ConversationalRetrievalChain.from_llm(
    llm=model,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)

def chat_history(request):
    """This function view returns the chat history"""
    try:
        print()
        print("We have been called")
        history = []
        messages = memory.chat_memory.messages
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append({
                    "user": messages[i].content,
                    "chat_bot": messages[i + 1].content
                })
        print("HISTORY IS:: ", history)
        return JsonResponse({"data": history}, safe=False)
    except Exception as e:
        print("Error is:: ", e)
        return JsonResponse({"status": 404, "error": "Unable to fetch history at this time"})
        
@csrf_exempt
def prompt(request):
    try:
        print("STarted")
        data = json.loads(request.body.decode('utf-8'))
        query = data.get("query")
        qa.invoke(query)
        history = []
        messages = memory.chat_memory.messages
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append({
                    "user": messages[i].content,
                    "chat_bot": messages[i + 1].content
                })
        print("RESPONSE IS:: ", history)
        return JsonResponse({"data": history})
    except Exception as e:
        print("Error is:: ", e)
        return JsonResponse({"status": 404, "error": "Unable to respond at this time"})