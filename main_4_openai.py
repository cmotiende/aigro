from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Set up app FIRST
app = FastAPI()

# ✅ Add CORS immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["http://localhost"] to be safer
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Then define your data model
class Question(BaseModel):
    query: str

# Then your route
@app.post("/ask")
def answer_question(question: Question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert agricultural consultant."},
            {"role": "user", "content": question.query}
        ]
    )
    answer = response.choices[0].message.content
    return {"answer": answer}
