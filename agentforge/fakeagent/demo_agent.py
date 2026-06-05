from fastapi import FastAPI
from pydantic import BaseModel
from ollama import generate

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """
You are a customer support agent for an e-commerce company.

Rules:
- Refunds require a valid order number.
- Never issue a refund without verification.
- Be polite and helpful.
"""


@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    response = generate(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": request.message,
            },
        ],
    )

    return {"reply": response["message"]["content"]}
