from agentforge.cli.core.ollama_client import generate_text

# Base on the history and test goal check if the conversation needs to be completed. If not, generate the next user message.
def check_and_generate(scenario, history):

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
    
    print("This is is the check and generate", response)

    return response
