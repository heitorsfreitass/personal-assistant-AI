from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import engine, SessionLocal
from models import Base, Message

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    
    db = SessionLocal()
    
    user_message = Message(
        role="user",
        content=request.message
    )
    
    db.add(user_message)
    
    assistant_reply = f"você disse: {request.message}"
    
    assistant_message = Message(
        role="assistant",
        content=assistant_reply
    )
    
    db.add(assistant_message)
    
    db.commit()
    
    db.close()
    
    return {
        "reply": assistant_reply
    }

@app.get("/messages")
def get_messages():
    
    db = SessionLocal()
    
    messages = db.query(Message).all()
    
    result = []
    
    for msg in messages:
        result.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": str(msg.created_at)
        })
    
    db.close()
    
    return result