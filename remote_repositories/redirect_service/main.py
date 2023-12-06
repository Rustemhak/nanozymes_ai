from fastapi import FastAPI
from pydantic import BaseModel
from src.chat import ChatGPT

app = FastAPI()

class GPTRequest(BaseModel):
    query: str
    instructions: str
    context: str
    previous_questions: str

class GPTResponse(BaseModel):
    llm_response: str

@app.post("/gpt_response", response_model=GPTResponse)
async def chatgpt_response(request: GPTRequest):
    llm = ChatGPT()
    llm_response = llm(
        query=request.query,
        instructions=request.instructions,
        context=request.context,
        previous_questions=request.previous_questions)
    return {"llm_response": llm_response}