import typer
import uuid
import json
from typing import Annotated

from agentforge.cli.core.loader import load_test_files, load_test_file

from agentforge.cli.core.scenario_generator import generate_scenarios

from agentforge.cli.core.simulator_step import check_and_generate

from agentforge.cli.core.executor import call_agent

from agentforge.cli.core.evaluator import evaluate
from rich.console import Console
from rich.panel import Panel
from rich import json as rich_json

console = Console()

app = typer.Typer()


MAX_TURNS_PER_SCENARIO = 2


@app.command()
def test(file_path: Annotated[str, typer.Argument()] = "agentforge/tests"):
    agent_live_url = "http://localhost:8000/chat"

    files = load_test_files(file_path)

    console.print(f"\nLoaded {len(files)} test file(s)\n", style="bold cyan")

    total_scenarios = 0
    passed_count = 0
    failed_count = 0

    all_results = []

    for file in files:

        console.rule(f"TEST FILE: {file}")

        data = load_test_file(file)

        domain = data["domain"]
        user_goal = data["user_goal"]
        risk_focus = data["risk_focus"]

        scenarios = generate_scenarios(
            domain,
            user_goal,
            risk_focus,
        )

        console.print(f"Generated {len(scenarios)} scenarios\n", style="cyan")

        for scenario_index, scenario in enumerate(scenarios, start=1):

            total_scenarios += 1

            console.rule(f"Scenario #{scenario_index}: {scenario['scenario']}")

            history = []

            session_id = str(uuid.uuid4())

            turns = 0

            while turns < MAX_TURNS_PER_SCENARIO:

                result = check_and_generate(
                    scenario,
                    history,
                )

                if result["action"] == "end":
                    print(f"Conversation ended: {result['reason']}")
                    break

                user_message = result["message"]

                console.print(Panel(user_message, title="USER", style="bold white"))

                assistant_reply = call_agent(
                    agent_live_url,
                    user_message,
                    session_id,
                )

                console.print(
                    Panel(assistant_reply, title="ASSISTANT", style="bold green")
                )

                history.append(
                    {
                        "role": "user",
                        "content": user_message,
                    }
                )

                history.append(
                    {
                        "role": "assistant",
                        "content": assistant_reply,
                    }
                )

                turns += 1

            if turns >= MAX_TURNS_PER_SCENARIO:
                console.print(
                    f"Reached max turns ({MAX_TURNS_PER_SCENARIO})", style="yellow"
                )

            evaluation = evaluate(
                test_definition=data,
                history=history,
                scenario=scenario,
            )

            passed = evaluation.get("passed", False)

            if passed:
                passed_count += 1
                status = "PASS"
            else:
                failed_count += 1
                status = "FAIL"

            scenario_result = {
                "file": file,
                "scenario": scenario["scenario"],
                "status": status,
                "evaluation": evaluation,
                "history": history,
            }

            all_results.append(scenario_result)

            console.print("\nEVALUATION", style="bold")
            try:
                console.print_json(data=json.dumps(evaluation))
            except Exception:
                console.print(evaluation)

            if passed:
                console.print(f"\nRESULT: {status}\n", style="bold green")
            else:
                console.print(f"\nRESULT: {status}\n", style="bold red")

    console.print("\n")
    console.rule("FINAL SUMMARY")

    console.print(f"Total scenarios: {total_scenarios}")
    console.print(f"Passed: {passed_count}")
    console.print(f"Failed: {failed_count}")

    success_rate = (passed_count / total_scenarios) * 100 if total_scenarios > 0 else 0

    console.print(f"Success Rate: {success_rate:.2f}%")

    if failed_count > 0:
        raise SystemExit(1)

    raise SystemExit(0)


if __name__ == "__main__":
    app()
