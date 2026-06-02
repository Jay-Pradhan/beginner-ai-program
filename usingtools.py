import os
from dotenv import load_dotenv

import json
from groq import Groq
import requests
from pydantic import BaseModel, Field

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("\n                                         *****WEATHER ASSITANT*****")


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
                   For a weather-related question where you have fetched weather data, respond in this exact JSON format:
                                {
                                "response": "Answer the user's question in about 30-40 words not giving the exact temperature, wind speed, etc."
                                "description": "Provide the actual and proper weather status with temperature, wind speed and also ask for any future updates(only once)",
                                } 

                    For any other response such as:

                        -Greeting("hi", "hello", or similar to that)
                        -Questions related to feel of the weather or the real life experience
                        -Non-weather related questions
                        -Follow-up conversation and reply

                    Just reply in plain text.

                    If the user asks a non-weather related question or something not related to weather, then just remind them that you are a weather assitant                                 
                """

messages = [{"role": "system", "content": system_prompt}]

while True:
    user = input("\nYou: ")

    if user.lower() in ["bye", "quit", "stop", "exit"]:
        print("Assistant: Bye :)")
        break

    messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools
    )

    response.model_dump()

    def call_function(name, args):
        if name == "weather":
            return weather(**args)

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            messages.append(response.choices[0].message)

            result = call_function(name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        class WeatherResponse(BaseModel):
            description: str = Field(description="Provide the weather conditions")
            response: str = Field(
                description="Address the user with the weather. For example: Sunny, Partly Cloud"
            )

        response_2 = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            response_format={"type": "json_object"},
        )

        raw_json = response_2.choices[0].message.content
        weather_report = WeatherResponse.model_validate_json(raw_json)

        print(f"Assistant: {weather_report.response}")
        print(f"Weather: {weather_report.description}")

        messages.append({"role": "assistant", "content": raw_json})

    else:
        reply = response.choices[0].message.content

        try:
            parsed = WeatherResponse.model_validate_json(reply)
            print(f"Assistant: {parsed.response}")
            print(f"Weather: {parsed.description}")
            messages.append({"role": "assistant", "content": reply})

        except Exception:
            print(f"Assistant: {reply}")
            messages.append({"role": "assistant", "content": reply})
