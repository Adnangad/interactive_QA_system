from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
from pydantic import BaseModel
from os import getenv

load_dotenv()

class Messages(BaseModel):
    role: str
    content: str


def generate_response(messages: list[Messages], model: OllamaLLM, query: str, chat_history)-> str:
    messages.append({"role": "user", "content": query})
    try:
        response = model.invoke(messages)
        messages.append({"role": "assistant", "content": response})
        chat_history.append({"user": query, "chat_bot": response})
        return chat_history
    except Exception as e:
        print("Error is:: ", e)
        return e
