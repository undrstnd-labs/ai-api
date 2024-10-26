from typing import Dict, Any
from api.database.client import SupabaseClient

class Requests:
    def __init__(self):
        self.client = SupabaseClient().client

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
