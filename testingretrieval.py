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
    user_input = input("Enter your question: ")

    if user_input in ["bye", "stop", "exit"]:
        print("Assistant: Bye:)")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools
    )
