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

    reply = generate(
        model="llama3",
        prompt=f"""
            {SYSTEM_PROMPT}

            User message: {request.message}

            Return ONLY valid JSON in this format:
            {{ "response": "string" }}
            """,
        format={
            "type": "object",
            "properties": {"response": {"type": "string"}},
            "required": ["response"],
        },
    )

    return {"response": reply["response"]}
