import typer

from agentforge.cli.core.loader import load_test_file
from agentforge.cli.core.executor import call_agent
from agentforge.cli.core.evaluator import evaluate

app = typer.Typer()



@app.command()
def test(file_path: str):
    # Load test file
    data = load_test_file(file_path)
    
    
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
