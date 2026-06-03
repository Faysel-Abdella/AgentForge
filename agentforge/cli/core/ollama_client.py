from ollama import generate


def generate_text(prompt: str):
    response = generate(model="llama3", prompt=prompt, stream=False)

    return response["response"]
