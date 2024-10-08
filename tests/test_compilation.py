import os
from openai import OpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()

    development_url = "http://localhost:3000/v1"
    production_url = "https://api.undrstnd-labs.com/v1"

    base_url = production_url if os.environ.get("ENV") == "production" else development_url

    is_streaming = False

    client = OpenAI(
        api_key="udsk_demo-api-key-x-00000",
        base_url=base_url
    )

    user_input = input("Enter a message: ")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama3-8b-8192",
        stream=is_streaming,
        max_tokens=1000,
    )

    if not is_streaming:
        print(chat_completion.choices[0].message.content)

    if is_streaming:
        for chunk in chat_completion:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n")
    print(chat_completion.to_dict()['usage'])

if __name__ == "__main__":
    main()
