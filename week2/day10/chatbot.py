import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI, HTTPException

from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import chat_with_profile

load_dotenv()

my_api_key=os.getenv("groq_api_key")

if not my_api_key:
    raise ValueError("Key kaha hai bhai/behen")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

app = FastAPI(title="JD Chatbot")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = chat_with_profile(request.message)
        return ChatResponse(answer=answer)
    except Exception as e:
        print(f"Chat error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response."
        )


# from services.knowledge_service import generate_profile
# from pathlib import Path

# resume_folder = Path("resumes") / "Resume_JaydeepGedam(latest).pdf"
# profile = generate_profile(resume_folder)
# print(profile)

