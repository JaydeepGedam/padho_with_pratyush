from pathlib import Path
import json

memory_file = Path("data") / "conversations.json"

def load_conversations():

    if not memory_file.exists():
        return {}

    with open(memory_file, "r", encoding="utf-8") as file:
        content = file.read().strip()

        if not content:
            return {}

        return json.loads(content)

def get_history(session_id: str) -> list:

    conversations = load_conversations()

    return conversations.get(session_id, [])


def save_message(session_id: str, role: str, content: str):

    conversations = load_conversations()

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({
        "role": role,
        "content": content
    })

    save_conversations(conversations)


def clear_history(session_id: str):

    conversations = load_conversations()

    conversations.pop(session_id, None)

    save_conversations(conversations)

def save_conversations(conversations):
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(conversations, file, indent=4)
