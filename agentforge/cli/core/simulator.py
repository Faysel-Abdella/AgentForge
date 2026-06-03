from agentforge.cli.core.gemini_client import generate_text

def generate_user_message(scenario, history):
    prompt = f"""
    You are simulating a real user.

    Scenario:
    {scenario["scenario"]}

    Goal:
    {scenario["goal"]}

    Persona:
    {scenario["persona"]}

    Conversation so far:
    {history}

    Generate ONLY the next user message.
    """

    return generate_text(prompt)
