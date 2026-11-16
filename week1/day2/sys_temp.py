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
prompt="I love you baby."

system_message={
    "role": "system",
    "content": "You are my office colleague and also my strict manager."
}

message={
    "role": role,
    "content": prompt 
}

messages= [system_message, message]
response = client.chat.completions.create(model=model, messages=messages, temperature=2)
print(response.choices[0].message.content)