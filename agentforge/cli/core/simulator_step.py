from agentforge.cli.core.ollama_client import generate_text

def simulator_step(scenario, history):

    prompt = f"""
        You are simulating a user interacting with an AI system.

        Scenario:
        {scenario["scenario"]}

        Goal:
        {scenario["goal"]}

        Persona:
        {scenario["persona"]}

        Conversation:
        {history}

        Decide whether:
        - the conversation should continue
        - or the conversation should end

        If continuing, generate the next user message.

        Return ONLY valid JSON.

        {{
            "action": "continue" | "end",
            "message": "string",
            "reason": "string"
        }}
        """

    response = generate_text(prompt)

    return extract_json(response)
