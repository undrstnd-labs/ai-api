from typing import Optional

from api.database.client import SupabaseClient


class ApiTokens:
    def __init__(self):
        self.client = SupabaseClient().client

    def get_api_key(self, id: str) -> Optional[dict]:
        response = self.client.table("api_tokens").select("*").eq("id", id).execute()
        api_key = response.data[0] if response.data else None
        return api_key
