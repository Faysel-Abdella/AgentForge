import httpx

def call_agent(endpoint: str, messages: list, session_id: int):
    resposne = httpx.post(endpoint, json={"message": messages, "session_id": session_id})

    data = resposne.json()

    return data["response"]
