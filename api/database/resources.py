from typing import Optional

from api.database.client import SupabaseClient


class Resources:
    def __init__(self):
        self.client = SupabaseClient().client

    async def get_resource(self, resource_id: str) -> Optional[dict]:
        resource = (
            await self.client.table("resources")
            .find_unique(where={"id": resource_id})
            .execute()
        )
        return resource
