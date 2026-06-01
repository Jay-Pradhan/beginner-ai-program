import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY")
)


class Details(BaseModel):
    name: str
    age: int


user_input = input("Provide us you details: ")

response = client.beta.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Extract the key details of the information. Respond only in JSON format only with keys-> name(string): and age(int):",
        },
        {"role": "user", "content": user_input},
    ],
    response_format={"type": "json_object"},
)

raw_json = response.choices[0].message.content
details = Details(**json.loads(raw_json))

print("----DETAILS----")
print(f"Name: {details.name}")
print(f"Age: {details.age}")
