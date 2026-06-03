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
