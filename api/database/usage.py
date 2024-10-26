from api.database.client import SupabaseClient


class Usage:
    def __init__(self):
        self.client = SupabaseClient().client

    async def create_usage(self, user_id: str, tokens_used: int, cost: float) -> dict:
        usage = (
            await self.client.table("usage")
            .create(
                data={
                    "userId": user_id,
                    "tokensUsed": tokens_used,
                    "cost": cost,
                }
            )
            .execute()
        )
        return usage

    async def update_usage(self, usage_id: str, tokens_used: int, cost: float) -> dict:
        usage = (
            await self.client.table("usage")
            .update(
                where={"id": usage_id}, data={"tokensUsed": tokens_used, "cost": cost}
            )
            .execute()
        )
        return usage
