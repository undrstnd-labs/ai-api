import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from starlette.responses import StreamingResponse

from api.database.funding import Fundings
from api.database.requests import Requests
from api.database.usage import Usage
from api.models.request import ChatCompletionRequest, CompletionRequest
from api.services.api_key import get_api_token_model_inference, retrieve_api_key
from api.services.models import ModelService
from api.services.response_generator import (
    generate_chat_completion,
    generate_completion,
    stream_chat_completion,
    stream_completion,
)

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
                    stream_chat_completion(
                        model=model,
                        client=client,
                        request=request,
                        api_token=api_token,
                        request_data=request_data,
                    ),
                    media_type="application/x-ndjson",
                )
            else:
                return generate_chat_completion(
                    model=model,
                    client=client,
                    request=request,
                    api_token=api_token,
                    request_data=request_data,
                )
        else:
            raise HTTPException(status_code=400, detail="ERROR: No messages provided")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error - {e}")


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
                    stream_completion(model=model, client=client, request=request),
                    media_type="application/x-ndjson",
                )
            else:
                return generate_completion(
                    client=client,
                    model=model,
                    request=request,
                    api_token=api_token,
                    request_data=request,
                )
        else:
            raise HTTPException(status_code=400, detail="ERROR: No prompt provided")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
