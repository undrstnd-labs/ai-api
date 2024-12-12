import asyncio
import json

from fastapi import HTTPException
from openai import OpenAI

from api.database.funding import Fundings
from api.database.requests import Requests
from api.database.usage import Usage
from api.models.request import ChatCompletionRequest, CompletionRequest
from api.models.type import Model, Request
from api.services.models import ModelService
from api.utils.label import clean_label

usage_db = Usage()
funding_db = Fundings()
requests_db = Requests()
model_service = ModelService()


async def stream_chat_completion(
    client: OpenAI,
    model: Model,
    request: ChatCompletionRequest,
    api_token: dict,
    request_data: Request,
):
    response = client.chat.completions.create(
        model=model,
        stream=True,
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user,
    )

    token_used = 0
    for chunk in response:
        chunk_data = clean_label(chunk.to_dict())
        token_used += 1
        yield f"data: {json.dumps(chunk_data)}\n\n"

    consumption = token_used * (model_service.get_model_pricing(model) / 1000000)
    funding = funding_db.get_funding(user_id=api_token["userId"])
    if not funding or funding["amount"] <= 0:
        requests_db.update_request(
            request_id=request_data.data[0]["id"],
            status="FAILED",
            response="ERROR: Insufficient balance.",
        )
        yield "data: [DONE]\n\n"
        raise Exception("Insufficient balance.")
    funding_db.update_funding(
        user_id=api_token["userId"],
        amount=funding["amount"] - consumption,
        currency=funding["currency"],
    )

    usage_db.create_usage(
        user_id=api_token["userId"],
        tokens_used=token_used,
        cost=consumption,
    )

    requests_db.update_request(
        request_id=request_data.data[0]["id"],
        status="SUCCESS",
    )

    yield "data: [DONE]\n\n"


async def stream_completion(
    client: OpenAI,
    model: str,
    request: CompletionRequest,
    api_token: dict,
    request_data: Request,
):
    response = client.completions.create(
        model=model,
        stream=True,
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user,
    )

    token_used = 0
    for chunk in response:
        chunk_data = clean_label(chunk.to_dict())
        token_used += 1
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)

    consumption = token_used * (model_service.get_model_pricing(model) / 1000000)
    funding = funding_db.get_funding(user_id=api_token["userId"])
    if not funding or funding["amount"] <= 0:
        requests_db.update_request(
            request_id=request_data.data[0]["id"],
            status="FAILED",
            response="ERROR: Insufficient balance.",
        )
        yield "data: [DONE]\n\n"
        raise Exception("Insufficient balance.")
    funding_db.update_funding(
        user_id=api_token["userId"],
        amount=funding["amount"] - consumption,
        currency=funding["currency"],
    )

    usage_db.create_usage(
        user_id=api_token["userId"],
        tokens_used=token_used,
        cost=consumption,
    )

    requests_db.update_request(
        request_id=request_data.data[0]["id"],
        status="SUCCESS",
    )

    yield "data: [DONE]\n\n"


def generate_chat_completion(
    client: OpenAI,
    model: Model,
    request: ChatCompletionRequest,
    api_token: dict,
    request_data: Request,
):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user,
        stream=False,
    )

    token_used = response.usage.total_tokens
    response = clean_label(response.to_dict())
    consumption = token_used * (model_service.get_model_pricing(model) / 1000000)

    funding = funding_db.get_funding(user_id=api_token["userId"])
    if not funding or funding["amount"] <= 0:
        requests_db.update_request(
            request_id=request_data.data[0]["id"],
            status="FAILED",
            response="ERROR: Insufficient balance.",
        )
        return HTTPException(status_code=402, detail="Insufficient balance.")

    funding_db.update_funding(
        user_id=api_token["userId"],
        amount=funding["amount"] - consumption,
        currency=funding["currency"],
    )

    usage_db.create_usage(
        user_id=api_token["userId"],
        tokens_used=token_used,
        cost=consumption,
    )

    requests_db.update_request(
        request_id=request_data.data[0]["id"],
        status="SUCCESS",
    )

    return response


def generate_completion(
    client: OpenAI,
    model: str,
    request: CompletionRequest,
    api_token: dict,
    request_data: Request,
):
    response = client.completions.create(
        model=model,
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stop=request.stop,
        n=request.n,
        logprobs=request.logprobs,
        user=request.user,
        stream=False,
    )

    token_used = response.usage.total_tokens
    response = clean_label(response.to_dict())
    consumption = token_used * (model_service.get_model_pricing(model) / 1000000)

    funding = funding_db.get_funding(user_id=api_token["userId"])
    if not funding or funding["amount"] <= 0:
        requests_db.update_request(
            request_id=request_data.data[0]["id"],
            status="FAILED",
            response="ERROR: Insufficient balance.",
        )
        return HTTPException(status_code=402, detail="Insufficient balance.")

    funding_db.update_funding(
        user_id=api_token["userId"],
        amount=funding["amount"] - consumption,
        currency=funding["currency"],
    )

    usage_db.create_usage(
        user_id=api_token["userId"],
        tokens_used=token_used,
        cost=consumption,
    )

    requests_db.update_request(
        request_id=request_data.data[0]["id"],
        status="SUCCESS",
    )

    return response
