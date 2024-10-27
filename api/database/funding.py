from typing import Optional

from api.database.client import SupabaseClient


class Fundings:
    def __init__(self):
        self.client = SupabaseClient().client

    def update_funding(
        self, user_id: str, amount: float, currency: str
    ) -> Optional[dict]:
        funding = (
            self.client.table("fundings")
            .update({"amount": amount, "currency": currency})
            .eq("userId", user_id)
            .execute()
        )
        return funding.data[0] if funding.data else None

    def get_funding(self, user_id: str) -> Optional[dict]:
        funding = (
            self.client.table("fundings").select("*").eq("userId", user_id).execute()
        )
        return funding.data[0] if funding.data else None
