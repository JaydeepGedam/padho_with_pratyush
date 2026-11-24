import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from schemas.chat import ClearChatRequest
from services.memory_service import clear_history
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import chat_with_profile

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

my_api_key=os.getenv("groq_api_key")

if not my_api_key:
    raise ValueError("Key kaha hai bhai/behen")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

app = FastAPI(title="JD Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # answer = chat_with_profile(
        #     request.message,
        #     request.session_id
        # )
        # return ChatResponse(answer=answer)
        return StreamingResponse(
            chat_with_profile(
                user_message=request.message,
                session_id=request.session_id
            ),
            media_type="text/plain"
        )
    except Exception as e:
        print(f"Chat error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response."
        )

@app.post("/chat/clear")
def clear_chat(request: ClearChatRequest):
    clear_history(request.session_id)

    return {
        "message": "Conversation history cleared successfully"
    }

# from services.knowledge_service import generate_profile
# from pathlib import Path

# resume_folder = Path("resumes") / "Resume_JaydeepGedam(latest).pdf"
# profile = generate_profile(resume_folder)
# print(profile)

