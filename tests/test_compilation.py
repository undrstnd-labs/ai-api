import os
from openai import OpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()

    development_url = "http://localhost:3000/v1"
    production_url = "https://ai-api-u74q.onrender.com/v1"

    base_url = production_url if os.environ.get("ENV") == "production" else development_url

    is_streaming = True

    client = OpenAI(
        api_key="udsk_demo-api-key-x-00000",
        base_url=base_url
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Give me a summary of the meaning of life",
            }
        ],
        model="llama3-8b-8192",
        stream=is_streaming
    )

    if not is_streaming:
        print(chat_completion.choices[0].message.content)

    if is_streaming:
        for chunk in chat_completion:
            print(chunk.choices[0].delta.content, end="", flush=True)

if __name__ == "__main__":
    main()
