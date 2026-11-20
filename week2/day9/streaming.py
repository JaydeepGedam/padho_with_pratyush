import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("groq_api_key")

if not my_api_key:
    raise ValueError("Key kaha hai bhai/behen")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"
prompt="Explain me human evaluation in detail."

message={
    "role": role,
    "content": prompt 
}

messages= [message]
# response = client.chat.completions.create(model=model, messages=messages)
# print(response.choices[0].message.content)

stream = client.chat.completions.create(model=model, messages=messages, stream=True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)