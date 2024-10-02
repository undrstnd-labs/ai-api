from typing import cast, Tuple
from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader

from prisma.models import APIToken

from api.models.type import Model
from api.database.db import Database
from api.services.model import ModelService
from api.models.inference import InferenceType, InferenceBaseUrl


async def retrieve_api_key(
    api_key_header: str = Depends(
        APIKeyHeader(name="Authorization", auto_error=False)
    )
) -> APIToken:
    """
    Retrieve the API token object from the database using the API key
    provided in the request header.

    :param api_key_header: The API key provided in the request header.
    :type api_key_header: str
    :return: The API token object if the API key is valid.
    :rtype: APIToken
    :raises HTTPException: If the API key is missing or invalid.
    """

    if api_key_header is None:
        print("API key is missing")
        raise HTTPException(
            status_code=403,
            detail="ERROR: API key is missing"
        )
    
    async with Database() as db:
        api_token = cast(APIToken, await db.get_api_key(api_key_header.split(" ")[1]))

    if api_token is None:
        print(f"Invalid API key: {api_key_header}")
        raise HTTPException(
            status_code=403,
            detail="ERROR: Invalid API token."
        )

    return api_token



async def get_api_token_model_inference(
            api_key: APIToken,
            model: str
        ) -> Tuple[Model, str, str]:
    """
    Retrieve the model object, inference type,
    and token based on the model name.

    :param api_key: The API token object.
    :type api_key: APIToken
    :param model: The model name.
    :type model: str
    :return: A tuple containing the model object, inference type, and token.
    :rtype: Tuple[Model, InferenceType, str]
    """

    model_service = ModelService()
    if model_service.get_model(model) is None:
        print(f"Model not found: {model}")
        raise HTTPException(
            status_code=404,
            detail="ERROR: Model not found."
        )
    if model_service.get_model_inference(model) == InferenceType.GR_LPU.value:
        return (
            model_service.get_model_id(model),
            api_key.tokenGr,
            InferenceBaseUrl.GR_LPU.value
        )

    elif (model_service.get_model_inference(model) == InferenceType.CR_INF.value):
        return (
                model_service.get_model_id(model),
                api_key.tokenCr,
                InferenceBaseUrl.CR_INF.value
            )

    elif (model_service.get_model_inference(model) == InferenceType.SM_RDU.value):
        return (
                model_service.get_model_id(model),
                api_key.tokenSm,
                InferenceBaseUrl.SM_RDU.value
            )

    raise HTTPException(
        status_code=400,
        detail="ERROR: Inference type not found."
    )
