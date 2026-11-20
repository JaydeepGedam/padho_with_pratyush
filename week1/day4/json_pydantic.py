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

from pydantic import BaseModel

class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema=Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema {schema} and give me a json output.
"""

message_system={
    "role": "system",
    "content": system_prompt
}

text="Hello my name is Jaydeep, i broke up with my girlfriend shital. i have an iphone which is not working at all. my address is delhi and my email id is abc@gmail.com. my contact number is 9876543456."

prompt=f"""This is the customer ticker, please extract personal information and give it to me {text}"""

message={
    "role": role,
    "content": prompt 
}

messages= [message_system , message]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
# print(response.choices[0].message.content)

# isko padhte kaise hai

import json
raw_json = response.choices[0].message.content
data_file = json.loads(raw_json)
ticket=Ticket(**data_file)
# print(type(ticket))
print(ticket.name)
print(ticket.email)
print(ticket.issue)