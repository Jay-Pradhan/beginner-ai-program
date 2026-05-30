from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say hello!"}],
)

print(response.choices[0].message.content)
