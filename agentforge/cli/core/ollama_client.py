from ollama import generate


def generate_text(prompt: str, responseFormat):
    response = generate(
        model="llama3", prompt=prompt, stream=False, format=responseFormat
    )

    return response["response"]
