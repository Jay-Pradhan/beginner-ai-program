import os
from dotenv import load_dotenv

import json
from openai import OpenAI
import requests
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY")
)


def weather(latitude, longitude):
    api = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    data = api.json()
    return data["current"]


tools = [
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Get the current situation of weather of the provided coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful a weather assistant, satisfy user's expectations"
# user_prompt = input("You: ")

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Tell me about the weather in bhubaneswar"},
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile", messages=messages, tools=tools
)


response.model_dump()


def call_function(name, args):
    if name == "weather":
        weather(**args)


for tool_call in response.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(response.choices[0].message)

result = call_function(name, args)
messages.append(
    {"role": "tool", "tool_call.id": tool_call.id, "content": json.dumps(result)}
)
