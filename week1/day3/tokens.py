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
prompt1="Hi"
prompt2="Explain me time travel in detail under 100 words"
prompt3="Write essay on human evaluation in 1000 words"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message={
        "role": role,
        "content": prompt 
    }

    messages= [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=500)
    # print(response.choices[0].message.content)
    usage = response.usage
    print(f"Prompt : {prompt} --> Your Tokens: {usage.prompt_tokens} Completion Tokens: {usage.completion_tokens}  Total Tokens: {usage.total_tokens}  Finish Reason: {response.choices[0].finish_reason}")