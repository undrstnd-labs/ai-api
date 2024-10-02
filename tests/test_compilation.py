from openai import OpenAI

client = OpenAI(
    api_key="udsk_demo-api-key-x-00000",
    base_url="http://localhost:3000/v1"
)

stream = True

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is meaning of life",
        }
    ],
    model="llama3-8b-8192",
    stream=stream
)

if not stream:
    print(chat_completion.choices[0].message.content)

if stream:
    for chunk in chat_completion:
        print(chunk.choices[0].delta.content, end="", flush=True)