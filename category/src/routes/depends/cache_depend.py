from fastapi import Depends
from src.infra.context.app_context import AppContext
from src.repo.redis.redis_repo import RedisCacheRepo
from redis import Redis

def cache_client_depend():
    client = AppContext.cache_client
    yield from client.get_dependency()
    
def cache_repo_depend(
    client: Redis = Depends(cache_client_depend)
) -> RedisCacheRepo:

    if isinstance(client, Redis):
        return RedisCacheRepo(client)