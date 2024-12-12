from openai import OpenAI
from api.services.api_key import get_api_token_model_inference

class ClientService:
    def __init__(self, api_token, model):
        self.api_token = api_token
        self.model = model
        self.client = None

    async def create_client(self):
        model, api_key, base_url = await get_api_token_model_inference(
            self.api_token, self.model
        )

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        
        return self.client, model
