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

model = OllamaLLM(model="llama3.1")

system_message = "You are an interactive QA system that provides accurate responses.You are also helpful and love using emojis to be more interactive."

llama_messages = [{"role": "system", "content": system_message}]


app = FastAPI()

class Prompt(BaseModel):
    query: str

class Response(BaseModel):
    role: str
    content: str

@app.post("/prompt", response_model=list[Response])
async def root(prompt: Prompt):
    try:
        response = generate_response(llama_messages, model, prompt.query)
        print(response)
        return response[1:]
    except Exception as e:
        print("Error is:: ", e)