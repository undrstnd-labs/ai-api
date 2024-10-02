from typing import Optional, Dict, Any
from prisma import Prisma
from prisma.models import Funding, APIToken, Request, Usage, Resource


class Database:
    def __init__(self):
        self.db = Prisma()

    async def __aenter__(self):
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.db.disconnect()

    async def update_funding(
                self,
                user_id: str,
                amount: float,
                currency: str
            ) -> Optional[Funding]:
        funding = await self.db.funding.update(
            where={'userId': user_id},
            data={'amount': amount, 'currency': currency}
        )
        return funding

    async def get_funding(self, user_id: str) -> Optional[Funding]:
        funding = await self.db.funding.find_unique(where={'userId': user_id})
        return funding

    async def get_api_key(self, id: str) -> Optional[APIToken]:
        api_key = await self.db.apitoken.find_first(where={'id': id})
        return api_key

    async def create_request(
                self,
                user_id: str,
                parameters: Dict[str, Any],
                request: Dict[str, Any],
                response: str,
                endpoint: str
            ) -> Request:
        request = await self.db.request.create(
            data={
                'userId': user_id,
                'parameters': parameters,
                'request': request,
                'response': response,
                'endpoint': endpoint,
            }
        )
        return request

    async def update_request(self, request_id: str, status: str) -> Request:
        request = await self.db.request.update(
            where={'id': request_id},
            data={'status': status}
        )
        return request

    async def create_usage(
                    self,
                    user_id: str,
                    tokens_used: int,
                    cost: float
                ) -> Usage:
        usage = await self.db.usage.create(
            data={
                'userId': user_id,
                'tokensUsed': tokens_used,
                'cost': cost,
            }
        )
        return usage

    async def update_usage(
                self,
                usage_id: str,
                tokens_used: int,
                cost: float
            ) -> Usage:
        usage = await self.db.usage.update(
            where={'id': usage_id},
            data={'tokensUsed': tokens_used, 'cost': cost}
        )
        return usage

    async def get_resource(self, resource_id: str) -> Optional[Resource]:
        resource = await self.db.resource.find_unique(
             where={'id': resource_id}
            )
        return resource
