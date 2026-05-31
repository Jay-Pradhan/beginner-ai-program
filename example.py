import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.environ.get("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Who is this?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDN_x3qsMAqlbRhBpGwv44hqQphdGCvCQkGD4hTuAww4EhMOVJyT2l55-hj2WMNBfit5ExLhwCdozA9eD-Ae2yCsqtFAoTvzu23yt80uCWrQ&s=10",
                    },
                },
            ],
        }
    ],
)


print(response.choices[0].message.content)
