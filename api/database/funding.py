from api.database.client import SupabaseClient
from typing import Optional

class Fundings:
    def __init__(self):
        self.client = SupabaseClient().client

    async def update_funding(self, user_id: str, amount: float, currency: str) -> Optional[dict]:
        funding = await self.client.table("fundings").update(
            where={'userId': user_id},
            data={'amount': amount, 'currency': currency}
        ).execute()
        return funding

    async def get_funding(self, user_id: str) -> Optional[dict]:
        funding = await self.client.table("fundings").find_unique(where={'userId': user_id}).execute()
        return funding
