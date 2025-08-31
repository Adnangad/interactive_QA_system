from fastapi import FastAPI
from pydantic import BaseModel
import json
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
from pydantic import BaseModel
from os import getenv
from llm import generate_response

load_dotenv()

class Messages(BaseModel):
    role: str
    content: str

class ChatHistory(BaseModel):
    user: str
    chat_bot: str

model = OllamaLLM(model="llama3.1")

system_message = "You are an interactive QA system that provides accurate responses.You are also helpful and love using emojis to be more interactive."

llama_messages = [{"role": "system", "content": system_message}]
chat_history: list[dict] = []


app = FastAPI()

class Prompt(BaseModel):
    query: str

class Response(BaseModel):
    role: str
    content: str

@app.post("/history", response_model=list[ChatHistory])
async def get_history():
    try:
        return chat_history
    except Exception as e:
        print("Error is:: ", e)

@app.post("/prompt", response_model=list[ChatHistory])
async def root(prompt: Prompt):
    try:
        print("STarted")
        response = generate_response(llama_messages, model, prompt.query, chat_history)
        print(response)
        return response
    except Exception as e:
        print("Error is:: ", e)
