
import os
from dotenv import load_dotenv
from groq import Groq
# from services.profile_tools import get_personal_info

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not API_KEY:
    raise ValueError("Groq API key not found!")

client = Groq(api_key=API_KEY)

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_personal_info",
#             "description": (
#                 "Retrieve the candidate's personal and professional "
#                 "summary, education, certifications and achievements."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": []
#             }
#         }
#     }
# ]

def generate_response(messages: list[dict]) -> str:

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # tools=tools,
        temperature=0.3,
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            # print(content)
            yield content
