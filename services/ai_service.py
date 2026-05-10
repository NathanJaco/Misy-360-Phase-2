from openai import OpenAI
import json
from pathlib import Path

def build_prompt(context_hint: str):
    return (
        "You are an AI assistant in an inventory management app for a small business. "
        "Use the inventory context to answer questions about current products, stock, categories, prices, and product actions. "
        "If the user asks about low stock, use the stock numbers from the context. "
        "There are not multiple locations, so do not ask about that. "
        "Do not ask the user to upload inventory because the app already provides inventory context. "
        "If the answer is not in the context, say you do not see it in the current inventory. "
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