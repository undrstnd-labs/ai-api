import os
from dotenv import load_dotenv
from supabase import create_client
from typing import Dict, Any, Optional

class Database:
    def __init__(self):
        load_dotenv()
        SUPABASE_URL = os.environ.get("SUPABASE_URL")
        SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
        self.client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    async def update_funding(self, user_id: str, amount: float, currency: str) -> Optional[dict]:
        funding = await self.client.table("fundings").update(
            where={'userId': user_id},
            data={'amount': amount, 'currency': currency}
        ).execute()
        return funding

    async def get_funding(self, user_id: str) -> Optional[dict]:
        funding = await self.client.table("fundings").find_unique(where={'userId': user_id}).execute()
        return funding

    async def get_api_key(self, id: str) -> Optional[dict]:
        response =  self.client.table("api_tokens").select("*").eq("id", id).execute()
        api_key = response.data[0] if response.data else None
        return api_key

    async def create_request(self, user_id: str, parameters: Dict[str, Any], request: Dict[str, Any], response: str, endpoint: str) -> dict:
        request = await self.client.table("requests").create(
            data={
                'userId': user_id,
                'parameters': parameters,
                'request': request,
                'response': response,
                'endpoint': endpoint,
            }
        ).execute()
        return request

    async def update_request(self, request_id: str, status: str) -> dict:
        request = await self.client.table("requests").update(
            where={'id': request_id},
            data={'status': status}
        ).execute()
        return request

    async def create_usage(self, user_id: str, tokens_used: int, cost: float) -> dict:
        usage = await self.client.table("usage").create(
            data={
                'userId': user_id,
                'tokensUsed': tokens_used,
                'cost': cost,
            }
        ).execute()
        return usage

    async def update_usage(self, usage_id: str, tokens_used: int, cost: float) -> dict:
        usage = await self.client.table("usage").update(
            where={'id': usage_id},
            data={'tokensUsed': tokens_used, 'cost': cost}
        ).execute()
        return usage

    async def get_resource(self, resource_id: str) -> Optional[dict]:
        resource = await self.client.table("resources").find_unique(where={'id': resource_id}).execute()
        return resource
