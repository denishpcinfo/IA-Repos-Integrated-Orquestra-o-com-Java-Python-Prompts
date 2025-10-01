import httpx
from ..settings import settings
async def call_mock(endpoint: str, payload: dict) -> dict:
    url = settings.http_tool_url
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json={"endpoint": endpoint, "payload": payload})
        r.raise_for_status()
        return r.json()
