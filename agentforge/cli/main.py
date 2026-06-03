import typer
from typing import Annotated

from agentforge.cli.core.loader import (load_test_files, load_test_file)
from agentforge.cli.core.executor import call_agent
from agentforge.cli.core.evaluator import evaluate

from agentforge.cli.core.scenario_generator import generate_scenarios
from agentforge.cli.core.simulator import generate_user_message

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
        
        # for scenario in scenarios:
        #     user_message = generate_user_message(scenario, [])
        #     reply = call_agent(agent_live_url, user_message)
            
        #     # Here I want to evaluate the reply, how to evaluate ?
        #     # Use llm-as-a-judge to evaluate = Take the user message, the reply 
        #     # and the rules to evaluate against and call another llm to score or say PASS
        #     # or FAIL
            
        #     # Maybe store the evaluation in an array to display later or show for
        #     # each cases the result of the evaluation. 
            
        
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
