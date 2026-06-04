from ollama import generate


def generate_text(prompt: str, format: object):
    response = generate(model="llama3", prompt=prompt, stream=False, format=format)

    return response["response"]
