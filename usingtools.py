import os
from dotenv import load_dotenv

import json
from groq import Groq
import requests
from pydantic import BaseModel, Field

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("\n                                         *****WEATHER ASSITANT*****\n")


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
            "description": "Get the current situation of weather and give a brief description about it",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
        },
    }
]

system_prompt = """You are a helpful a weather assistant, satisfy user's expectations.
                   Respond only in this JSON format:
                                {
                                "description": "natural language for a weather description",
                                "response": "describe about it's beauty and any other unique feature"
                                } 
                """
user_prompt = input("You: ")
print()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile", messages=messages, tools=tools
)


response.model_dump()


def call_function(name, args):
    if name == "weather":
        return weather(**args)


for tool_call in response.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(response.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


class WeatherResponse(BaseModel):
    description: str = Field(description="Natural language for a weather description")
    response: str = Field(
        description="Describe about it's beauty and any other unique feature"
    )


response_2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    response_format={"type": "json_object"},
)

raw_json = response_2.choices[0].message.content
weather_report = WeatherResponse.model_validate_json(raw_json)

print("Assistant: ", end="")
print(weather_report.description)
print(weather_report.response)
