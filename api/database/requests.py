from typing import Any, Dict

from api.database.client import SupabaseClient
from api.utils.uuid import generate_uuid


class Requests:
    def __init__(self):
        self.client = SupabaseClient().client

    def create_request(
        self,
        user_id: str,
        parameters: Dict[str, Any],
        request: Dict[str, Any],
        response: str,
        endpoint: str,
    ) -> dict:
        print("user_id", user_id)
        print("parameters", parameters)
        print("request", request)
        print("response", response)
        print("endpoint", endpoint)
        request = (
            self.client.table("requests")
            .insert(
                {
                    "id": generate_uuid(),
                    "userId": user_id,
                    "parameters": parameters,
                    "request": request,
                    "response": response,
                    "endpoint": endpoint,
                }
            )
            .execute()
        )
        return request

    def update_request(self, request_id: str, status: str) -> dict:
        request = (
            self.client.table("requests")
            .update({"status": status})
            .eq("id", request_id)
            .execute()
        )
        return request
