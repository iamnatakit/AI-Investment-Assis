from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI(title="Project 1: Baseline Investment AI")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
    cost: float
    latency_seconds: float

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    
    # TODO: Implement Single Large Prompt Logic here
    # TODO: Implement Single LLM call here (e.g., OpenAI or OpenRouter API)
    # TODO: Calculate Token and Cost
    # TODO: Save Chat History, Token, and Cost Logs
    
    # Mock Response for now
    time.sleep(1) # simulate processing time
    latency = time.time() - start_time
    
    return ChatResponse(
        reply=f"Baseline Agent Received: {request.message}\n(This is a placeholder response)",
        tokens_used=150,
        cost=0.0015,
        latency_seconds=latency
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
