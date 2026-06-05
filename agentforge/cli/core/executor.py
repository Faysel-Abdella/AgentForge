import httpx

def call_agent(endpoint: str, messages: list, session_id: int):
    try:
        resposne = httpx.post(endpoint, json={"message": messages, "session_id": session_id})

        resposne.raise_for_status()
    except httpx.HTTPError as general_err:
        raise RuntimeError(f"A network error occurred {general_err}")
    else:
        data = resposne.json()
        print("This is the agent response", data)
        return data["response"]
