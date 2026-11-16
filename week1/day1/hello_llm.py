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
prompt="Do you know Virat Kohli, if yes can you tell me his birth date?"

message={
    "role": role,
    "content": prompt 
}

messages= [message]
response = client.chat.completions.create(model=model, messages=messages)
print(response.choices[0].message.content)