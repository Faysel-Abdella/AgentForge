import json

from agentforge.cli.core.ollama_client import generate_text


# Base on the history and test goal check if the conversation needs to be completed. If not, generate the next user message.
def check_and_generate(scenario, history):

    print(type(scenario))
    print(scenario)

    prompt = f"""
        You are simulating ONLY the USER in a conversation with an AI system.

        SCENARIO:
        {scenario["scenario"]}

        USER GOAL:
        {scenario["goal"]}

        USER PERSONA:
        {scenario["persona"]}

        CONVERSATION HISTORY:
        {history}

        IMPORTANT RULES:

        - You are the USER.
        - You must NEVER act as the assistant.
        - You must NEVER generate assistant responses.
        - You must NEVER ask the assistant for information on behalf of the assistant.
        - You must ONLY generate what the USER would say next.
        - Stay consistent with the persona and goal.
        - Use the conversation history to determine the next USER response.

        Your task:

        1. Decide whether the conversation should continue.
        2. If it should continue, generate the next USER message.
        3. If the goal has been achieved, the user has given up, or no meaningful progress can be made, end the conversation.

        OUTPUT RULES:

        - Return ONLY valid JSON.
        - Do NOT include markdown.
        - Do NOT include explanations.
        - Do NOT include text before or after the JSON.

        JSON SCHEMA:

        {{
            "action": "continue" | "end",
            "message": "next USER message only",
            "reason": "short explanation"
        }}

        EXAMPLE VALID OUTPUT:

        {{
            "action": "continue",
            "message": "I don't have my order number anymore. Is there another way to verify my purchase?",
            "reason": "Trying another approach to achieve the goal"
        }}
    """

    response = generate_text(
        prompt,
        {
            "type": "object",
            "properties": {
                "action": {"type": "string"},
                "message": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["action", "message", "reason"],
        },
    )

    print("This is is the check and generate", response)
    print("This is is the check and  json", json.loads(response))

    return json.loads(response)
