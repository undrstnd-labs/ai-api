import logging

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from starlette.responses import StreamingResponse

from api.models.request import AudioTranscriptions, AudioTranslations
from api.services.api_key import get_api_token_model_inference, retrieve_api_key
from api.services.response_generator import stream_chat_completion, stream_completion

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/audio/transcriptions", dependencies=[Depends(retrieve_api_key)])
async def chat_completions(
    request: AudioTranscriptions, api_token=Depends(retrieve_api_key)
):
    try:
        model, api_key, base_url = await get_api_token_model_inference(
            api_token, request.model
        )

        client = OpenAI(api_key=api_key, base_url=base_url)

        if request.messages:
            if request.stream:
                return StreamingResponse(
                    stream_chat_completion(model=model, client=client, request=request),
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
                return response
        else:
            return HTTPException(status_code=400, detail="ERROR: No messages provided")
    except Exception as e:
        logger.error(f"Error in chat_completions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/v1/audio/translations", dependencies=[Depends(retrieve_api_key)])
async def completions(request: AudioTranslations, api_token=Depends(retrieve_api_key)):
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
