from api.database.client import SupabaseClient
from api.utils.uuid import generate_uuid


class Usage:
    def __init__(self):
        self.client = SupabaseClient().client

    def create_usage(self, user_id: str, tokens_used: int, cost: float) -> dict:
        usage = (
            self.client.table("usages")
            .insert(
                {
                    "id": generate_uuid(),
                    "userId": user_id,
                    "tokensUsed": tokens_used,
                    "cost": cost,
                }
            )
            .execute()
        )
        return usage

    def update_usage(self, usage_id: str, tokens_used: int, cost: float) -> dict:
        usage = (
            self.client.table("usages")
            .update({"tokensUsed": tokens_used, "cost": cost})
            .eq("id", usage_id)
            .execute()
        )
        return usage
