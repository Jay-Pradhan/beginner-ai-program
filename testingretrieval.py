import os
from dotenv import load_dotenv

import json
from groq import Groq
from pydantic import BaseModel, Field

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_questions():
    with open("iplKB.json", "r") as f:
        return json.load(f)


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_questions",
            "description": "Get the answers to the user's question from the iplKB.json knowlege base",
            "parameters": {
                "type": "object",
                "properties": {"questions": {"type": "string"}},
                "required": ["questions"],
                "additionalProperties": False,
            },
        },
    }
]

system_prompt = """You are a helpful IPL assitant. You will provide the answers to the user's question from the IPL knowlege base

                   Willingly ask the user if he wants answer to any other querry

                   For any question not in the IPL knowlege base, just tell the user about your limitations 
"""

messages = [{"role": "system", "content": system_prompt}]

while True:
    # user_input = input("Enter your question: ")

    # if user_input in ["bye", "stop", "exit"]:
    # print("Assistant: Bye:)")
    # break

    messages.append(
        {
            "role": "user",
            "content": "Which player has taken the most wickets in IPL history?",
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools
    )

    response.model_dump()

    def call_function(name, args):
        if name == "get_questions":
            return get_questions(**args)

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = call_function(name, args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call.id": tool_call.id,
                    "content": json.dumps(result),
                }
            )
