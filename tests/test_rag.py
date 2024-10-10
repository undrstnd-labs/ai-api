import os, json, httpx
from openai import OpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()

    development_url = "http://localhost:8000/v1"
    production_url = "https://api.undrstnd-labs.com/v1"

    base_url = production_url if os.environ.get("ENV") == "production" else development_url

    is_streaming = True

    client = OpenAI(
        api_key="udsk_demo-api-key-x-00000",
        base_url=base_url
    )

    user_input = "Hello there"
    response = client.post(
        "/rag/chat/completions",
        cast_to=httpx.Response,
        body={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 600,
            "stream": is_streaming
        },
    )

    if not is_streaming:
        chat_completion = response.json()
        print(chat_completion['choices'][0]['message']['content'])
        print("\n")
        print(chat_completion['usage'])

 
    if is_streaming:
        chunks = response.text.split('data: ')
        for chunk in chunks[1:]:  # Skip the first empty chunk
            chunk_json = json.loads(chunk)
            print(chunk_json['choices'][0]['delta']['content'], end="", flush=True)

            if 'finish_reason' in chunk_json['choices'][0] and chunk_json['choices'][0]['finish_reason'] == 'stop':
                break

if __name__ == "__main__":
    main()
