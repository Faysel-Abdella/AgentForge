import typer
from typing import Annotated
import uuid

from agentforge.cli.core.loader import load_test_files, load_test_file
from agentforge.cli.core.executor import call_agent
from agentforge.cli.core.evaluator import evaluate

from agentforge.cli.core.scenario_generator import generate_scenarios
from agentforge.cli.core.simulator_step import check_and_generate

app = typer.Typer()


@app.command()
def test(file_path: Annotated[str, typer.Argument] = "agentforge/tests"):
    agent_live_url = "http://localhost:8000/chat"

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

        print("This is scenario", scenarios)

        for scenario in scenarios:
            history = []
            session_id = str(uuid.uuid4())

            while True:

                # Check if the conversation needs to be completed. If not, generate the next user message.
                result = check_and_generate(scenario, history)

                if result["action"] == "end":
                    break

                user_message = result["message"]

                reply = call_agent(agent_live_url, user_message, session_id)

                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": reply})

                print(f"This is the histiry {history}")

            # After all the turns for one scenario is completed, start the evaluation.
            evaluation_result = evaluate(data, history, scenario.get("scenario", ""))
            print("Evaluation result:", evaluation_result)

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
