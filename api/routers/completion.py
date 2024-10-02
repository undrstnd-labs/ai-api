import logging
from openai import OpenAI
from prisma.models import APIToken
from starlette.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Depends
from api.models.request import ChatCompletionRequest, CompletionRequest
from api.services.api_key import retrieve_api_key, get_api_token_model_inference
from api.services.async_generator import async_generator_chat_completion, async_generator_completion

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/v1/chat/completions",
    dependencies=[Depends(retrieve_api_key)]
)
async def chat_completions(
    request: ChatCompletionRequest,
    api_token: APIToken = Depends(retrieve_api_key)
):
    try:
        model, api_key, base_url = await get_api_token_model_inference(
            api_token, request.model
        )

        client = OpenAI(api_key=api_key, base_url=base_url)

        if request.messages:
            if request.stream:
                return StreamingResponse(
                    async_generator_chat_completion(
                        model=model,
                        client=client,
                        messages=request.messages,
                        max_tokens=request.max_tokens,
                        temperature=request.temperature,
                        top_p=request.top_p,
                        frequency_penalty=request.frequency_penalty,
                        presence_penalty=request.presence_penalty,
                        stop=request.stop,
                        n=request.n,
                        logprobs=request.logprobs,
                        user=request.user,
                        system=request.system,
                    ), media_type="application/x-ndjson"
                )
            else:
                response = client.chat.completions.create(
                    model=model,
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
                    user=request.user,
                    stream=False,
                )
                return response
        else:
            return HTTPException(
                status_code=400, 
                detail="ERROR: No messages provided"
            )
    except Exception as e:
        logger.error(f"Error in chat_completions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/v1/completions",
    dependencies=[Depends(retrieve_api_key)]
)
async def completions(
    request: CompletionRequest,
    api_token: APIToken = Depends(retrieve_api_key)
):
    try:
        model, api_key, base_url = await get_api_token_model_inference(
            api_token, request.model
        )

        client = OpenAI(api_key, base_url)

        if request.prompt:
            if request.stream:
                return StreamingResponse(
                    async_generator_completion(
                        model=model,
                        client=client,
                        system=request.system,
                        prompt=request.prompt,
                        max_tokens=request.max_tokens,
                        temperature=request.temperature,
                        top_p=request.top_p,
                        frequency_penalty=request.frequency_penalty,
                        presence_penalty=request.presence_penalty,
                        stop=request.stop,
                        n=request.n,
                        logprobs=request.logprobs,
                        user=request.user
                    ), media_type="application/x-ndjson"
                )
            else:
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
                    echo=request.echo,
                    user=request.user,
                    stream=False,
                )
                return response
        else:
            return HTTPException(status_code=400, detail="ERROR: No prompt provided")
    except Exception as e:
        logger.error(f"Error in completions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
