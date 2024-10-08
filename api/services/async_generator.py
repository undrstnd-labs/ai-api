import json
import asyncio
from openai import OpenAI

from api.models.request import ChatCompletionRequest, CompletionRequest


async def async_generator_chat_completion(
        client: OpenAI,
        model: str,
        request: ChatCompletionRequest
        ):
    response = client.chat.completions.create(
        model=model,
        stream=True,
        messages=[
            {"role": m.role, "content": m.content}
            for m in request.messages
        ],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user
    )

    for chunk in response:
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"



async def async_generator_completion(
        client: OpenAI,
        model: str,
        request: CompletionRequest
        ):
    response = client.completions.create(
        model=model,
        stream=True,
        messages=[
            {"role": "system", "content": request.system},
            {"role": m.role, "content": m.content}
            for m in request.messages
        ],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user
    )

    for chunk in response:
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"
