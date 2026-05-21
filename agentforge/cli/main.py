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


def evaluate(response: str, rules: list):
    for rule in rules:
        print(rule)

        # RULE 1: must_not_contain
        if rule["type"] == "must_not_contain":
            for word in rule["value"]:
                if word.lower() in response.lower():
                    return False

        # RULE 2: must_contain
        if rule["type"] == "must_contain":
            for word in rule["value"]:
                if word.lower() not in response.lower():
                    return False

    return True


@app.command()
def test(file_path: str):
    # Load test file
    file = open(file_path, "r")
    content = file.read()
    data = json.loads(content)

    # Extract the conversation and rules
    conversation = data["conversation"]
    rules = data["rules"]

    url = "https://6a0ebe061736097c360a69e8.mockapi.io/chat/chat"

    reply = call_agent(url, conversation)
    passed = evaluate(reply, rules)

    print("\nAgent response:\n")
    print(reply)

    print("\nResult:\n")
    if passed:
        print("PASS")
    else:
        print("FAIL")


if __name__ == "__main__":
    app()
