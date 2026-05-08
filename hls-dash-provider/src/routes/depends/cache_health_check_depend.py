from fastapi import Depends
from .cache_depend import cache_client_depend
from redis import Redis

async def cache_health_check_depend(
    client: Redis = Depends(cache_client_depend)
) -> bool:
    if isinstance(client, Redis):
        try:
            return client.ping()
        except:
            return False