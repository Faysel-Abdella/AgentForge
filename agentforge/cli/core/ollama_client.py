from ollama import generate


def generate_text(prompt: str):
    response = generate(
        model="llama3",
        prompt=prompt,
        stream=False,
        format={
            "type": "object",
            "properties": {
                "action": {"type": "string"},
                "message": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["action", "message", "reason"],
        },
    )

    return response["response"]
