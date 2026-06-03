import typer
from typing import Annotated

from agentforge.cli.core.loader import (load_test_files, load_test_file)
from agentforge.cli.core.executor import call_agent
from agentforge.cli.core.evaluator import evaluate

from agentforge.cli.core.scenario_generator import generate_scenarios
from agentforge.cli.core.simulator import generate_user_message
from agentforge.cli.core.check_conversation_continue import check_conversation_continue

app = typer.Typer()

@app.command()
def test(file_path: Annotated[str, typer.Argument] = "agentforge/tests"):
    agent_live_url = "https://6a0ebe061736097c360a69e8.mockapi.io/chat/chat"

    files = load_test_files(file_path)

    print("Files", files)

    passed_count = 0
    failed_count = 0

    for file in files:

        # Load test file
        data = load_test_file(file)

        # Extract the goal and the risks
        domain = data["domain"]
        user_goal = data["user_goal"]
        risk_focus = data["risk_focus"]

        # Get testing scenarios based on goal and risks
        scenarios = generate_scenarios(domain, user_goal, risk_focus)

        for scenario in scenarios:
            history = []
            keep_conversation = True

            while keep_conversation: 
                user_message = generate_user_message(scenario, [])
                reply = call_agent(agent_live_url, user_message)

                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": reply}) 

                # Check if the conversation needs to continue (Use LLM)
                keep_conversation = check_conversation_continue(history)
                
            # After all the turns for one scenario is completed, start the evaluation.
            evaluate(history)

            

        print(scenarios)

    #     reply = call_agent(agent_live_url, conversation)
    #     passed = evaluate(reply, rules)

    #     print(f"\nTEST FILE: {file}")

    #     if passed:
    #         passed_count += 1
    #         print("STATUS: PASS")
    #     else:
    #         failed_count += 1
    #         print("STATUS: FAIL")

    # print("\nSUMMARY")
    # print(f"PASSED: {passed_count}")
    # print(f"FAILED: {failed_count}")

    if failed_count > 0:
        raise SystemExit(1)
    raise SystemExit(0)

if __name__ == "__main__":
    app()
