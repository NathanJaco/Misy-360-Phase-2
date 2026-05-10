from openai import OpenAI
import json
from pathlib import Path

def build_prompt(context_hint: str):
    return (
        "You are an AI assistant in an inventory management app for a small business. "
        "Help users with product stock, categories, prices, adding products, updating products, and deleting products. "
        "If the user asks about prior conversation, use the chat history when possible. "
        f"This is the context hint: {context_hint}"
    )


def get_ai_response(client: OpenAI, chat_history: list, context_hint: str):
    prompt = build_prompt(context_hint)

    prompt_message = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    messages = chat_history + prompt_message

    ai_response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        temperature=1
    )

    return ai_response.choices[0].message.content


def load_logs(filepath: str):
    json_path = Path(filepath)

    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return []


def save_logs(filepath: str, logs: list):
    json_path = Path(filepath)

    with open(json_path, "w") as f:
        json.dump(logs, f)