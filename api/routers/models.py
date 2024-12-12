from fastapi import APIRouter, Depends

from api.services.api_key import retrieve_api_key
from api.services.models import ModelService

router = APIRouter()
model_service = ModelService()


@router.post("/v1/models", dependencies=[Depends(retrieve_api_key)])
async def get_models():
    """
    Retrieve the list of models available for completion.

    :return: A list of model objects.
    :rtype: List[Model]
    """
    model_info = model_service.get_model_info("llama-3.3-70b")
    return model_info
