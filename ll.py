import json
import requests

LM_API_URL = "http://172.16.122.48:1234/v1/chat/completions"
MODEL = "qwen2.5-coder-3b-instruct-mlx"


def call_llm_for_info(text):

    headers = {"Content-Type": "application/json"}

    prompt = f"""
Extract the transaction details from the text below.

Return ONLY this exact format. EACH FIELD MUST BE ON ITS OWN LINE.
NO quotes, NO commas, NO JSON, NO extra text, NO code blocks.

txn_id:
description:
clean_description:
merchant_name:
merchant_type:
payment_channel:
amount:
type:
date:
weekday:
time_of_day:
balance_after_txn:
category:
subcategory:
transaction_mode:
is_recurring:
recurrence_interval:
confidence_score:
is_high_value:
is_suspicious:
embedding_version:

Text:
{text}
    """

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }

    response = requests.post(LM_API_URL, headers=headers, json=body, timeout=30)
    print("RAW:", response.text)

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def parse_info_to_dict(info_text):
    result = {}

    for line in info_text.split("\n"):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()

    return result


def append_to_json_file(data, path="transactions.json"):
    try:
        with open(path, "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []

    existing.append(data)

    with open(path, "w") as f:
        json.dump(existing, f, indent=2)

    print("✔ Saved transaction to JSON")


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":

    sample_text = """
    Rs 554.50 debited from your account via UPI to INDIANRAILWAYCA848140
    on 01 Apr at 18:23. Avl Bal: 7827.12
    """

    info = call_llm_for_info(sample_text)
    print("\nLLM OUTPUT:\n", info)

    parsed = parse_info_to_dict(info)
    print("\nConverted to dict:\n", parsed)

    append_to_json_file(parsed)