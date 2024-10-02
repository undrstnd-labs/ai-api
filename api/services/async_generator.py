import json
import asyncio
from openai import OpenAI
from typing import List, Optional, Union

from api.models.request import Message


async def async_generator_chat_completion(
        client: OpenAI,
        messages: Optional[List[Message]],
        system: Optional[str],
        model: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
        stop: Optional[Union[str, List[str]]],
        n: int,
        logprobs: Optional[int],
        user: Optional[str]
        ):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": m.role, "content": m.content} for m in messages],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
        n=n,
        logprobs=logprobs,
        user=user,
        stream=True,
    )

    for chunk in response:
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"



async def async_generator_completion(
        client,
        prompt: Optional[str],
        model: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
        stop: Optional[Union[str, List[str]]],
        n: int,
        logprobs: Optional[int],
        user: Optional[str]
        ):
    response = client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
        n=n,
        logprobs=logprobs,
        user=user,
        stream=True,
    )

    for chunk in response:
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"
