import typer
import json
import httpx

app = typer.Typer()


def call_agent(endpoint: str, messages: list):
    try:  
        response = httpx.post(endpoint, json={"messages": messages})
        # "messages": [{role: 'user', 'content': 'I want a refund'}]
    except Exception as e:
        print(f"Error sending the request: {e}")

    return response.json()["response"]


@app.command()
def test(file_path: str):
    # Load test file
    file = open(file_path, "r")
    content = file.read()
    data = json.loads(content)

    # Extract the conversation
    conversation = data["conversation"]

    url = "https://6a0ebe061736097c360a69e8.mockapi.io/chat/chat"

    reply = call_agent(url, conversation)

    print("\nAgent Reply:\n")
    print(reply)


if __name__ == "__main__":
    app()
