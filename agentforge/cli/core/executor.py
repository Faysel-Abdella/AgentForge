import httpx

def call_agent(endpoint: str, messages: list):
    resposne = httpx.post(endpoint, json={"message": messages})

    data = resposne.json()

    return data["response"]
