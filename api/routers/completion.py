import logging

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from starlette.responses import StreamingResponse

from api.database.funding import Fundings
from api.database.requests import Requests
from api.database.usage import Usage
from api.models.request import ChatCompletionRequest, CompletionRequest
from api.services.api_key import get_api_token_model_inference, retrieve_api_key
from api.services.async_generator import (
    async_generator_chat_completion,
    async_generator_completion,
)
from api.services.models import ModelService

logger = logging.getLogger(__name__)

router = APIRouter()
usage_db = Usage()
funding_db = Fundings()
requests_db = Requests()
model_service = ModelService()


@router.post("/v1/chat/completions", dependencies=[Depends(retrieve_api_key)])
async def chat_completions(
    request: ChatCompletionRequest, api_token=Depends(retrieve_api_key)
):
    try:
        model, api_key, base_url = await get_api_token_model_inference(
            api_token, request.model
        )

        client = OpenAI(api_key=api_key, base_url=base_url)

        if request.messages:
            request_data = requests_db.create_request(
                user_id=api_token["userId"],
                parameters=request.model_dump(),
                request=request.model_dump(),
                response="PENDING: Request in progress.",
                endpoint="/v1/chat/completions",
            )

            if request.stream:
                return StreamingResponse(
                    async_generator_chat_completion(
                        model=model, client=client, request=request, api_token=api_token
                    ),
                    media_type="application/x-ndjson",
                )
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": m.role, "content": m.content} for m in request.messages
                    ],
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
                consumption = token_used * (
                    model_service.get_model_pricing(model) / 1000000
                )

                funding = funding_db.get_funding(user_id=api_token["userId"])
                if not funding or funding["amount"] <= 0:
                    requests_db.update_request(
                        request_id=request_data.data[0]["id"],
                        status="FAILED",
                        response="ERROR: Insufficient balance.",
                    )
                    return HTTPException(
                        status_code=402, detail="Insufficient balance."
                    )

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
        else:
            return HTTPException(status_code=400, detail="ERROR: No messages provided")
    except Exception as e:
        logger.error(f"Error in chat_completions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/v1/completions", dependencies=[Depends(retrieve_api_key)])
async def completions(request: CompletionRequest, api_token=Depends(retrieve_api_key)):
    try:
        model, api_key, base_url = await get_api_token_model_inference(
            api_token, request.model
        )

        client = OpenAI(api_key=api_key, base_url=base_url)

        if request.prompt:
            if request.stream:
                return StreamingResponse(
                    async_generator_completion(
                        model=model, client=client, request=request
                    ),
                    media_type="application/x-ndjson",
                )
            else:
                response = client.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": request.prompt},
                        *[
                            {"role": m.role, "content": m.content}
                            for m in request.messages
                        ],
                    ],
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
                return response
        else:
            return HTTPException(status_code=400, detail="ERROR: No prompt provided")
    except Exception as e:
        logger.error(f"Error in completions: {e}")
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
