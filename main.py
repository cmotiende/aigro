from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    query: str

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

@app.post("/ask")
def answer_question(question: Question):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": "You are an expert agricultural consultant. Help farmers with clear, useful answers."},
            {"role": "user", "content": question.query}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        return {"answer": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
