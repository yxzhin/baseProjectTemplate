from aiohttp import ClientSession

from ..conf import Config


class APIClient:
    def __init__(self):
        self.base_url = Config.API_URL

    async def start(self):
        self.session = ClientSession()

    async def get(self, path: str, **kwargs):
        async with self.session.get(self.base_url + path, **kwargs) as r:
            r.raise_for_status()
            return await r.json()

    async def close(self):
        await self.session.close()
