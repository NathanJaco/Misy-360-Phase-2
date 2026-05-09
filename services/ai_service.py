from openai import OpenAI
import json
from pathlib import Path

def build_ai_prompt(context):
    return "" \
    "You are a helpful inventory assistant for a small business inventory manager. " \
    "Answer user questions based on the inventory context provided. " \
    "Help users understand stock levels, categories, product updates, and inventory actions. " \
    "Keep answers clear and useful. " \
    f"This is my context: {context}"


def get_ai_response(client: OpenAI, chat_history: list, context: str):
    ai_prompt = build_ai_prompt(context)

    ai_prompt_message = [
        {
            "role": "system",
            "content": ai_prompt
        }
    ]

    messages = ai_prompt_message + chat_history

    ai_response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        temperature=1
    )

    return ai_response.choices[0].message.content


def build_inventory_context(products):
    context = "Current inventory products: "

    for product in products:
        context += (
            f"{product['name']} "
            f"category {product['category']} "
            f"price {product['price']} "
            f"stock {product['stock']}; "
        )

    return context

def load_logs(filepath):
    json_path = Path(filepath)

    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)

    return []


def save_logs(filepath, logs):
    json_path = Path(filepath)

    with open(json_path, "w") as f:
        json.dump(logs, f)