import os

import httpx
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()

    development_url = "http://localhost:8000/v1"
    production_url = "https://api.undrstnd-labs.com/v1"

    base_url = (
        production_url if os.environ.get("ENV") == "production" else development_url
    )

    is_streaming = True

    client = OpenAI(api_key="udsk_demo-api-key-x-00000", base_url=base_url)

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the purpose of life?"},
        ],
        max_tokens=600,
        stream=is_streaming,
    )

    if not is_streaming:
        print(chat_completion.choices[0].message.content)
        print("\n")
        print(chat_completion.to_dict()["usage"])

    if is_streaming:
        for chunk in chat_completion:
            print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == "__main__":
    main()
