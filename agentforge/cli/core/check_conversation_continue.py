from ollama import generate

def check_conversation_continue(history: list):
    prompt: f"""
    
    
    """
    
    keep: bool = generate(model="llama3", prompt=prompt, stream=False)
    
    return keep