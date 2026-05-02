from src.infra.cache.redis.connection import init_redis_client
from src.infra.schemas.database.redis import RedisParams, RedisClient

async def redis_bootstrap(
    params: RedisParams,
) -> RedisClient:

    client = init_redis_client(
        params.host,
        params.port,
        params.password,
    )
    
    return RedisClient(
        params=params,
        client=client,
    )
    
async def init_cache_client(
    params: RedisParams,
) -> RedisClient:
    
    return await redis_bootstrap(params)
    
    
async def terminate_cache_client(
    context: RedisClient,
):

    if not context:
        return
    
    if isinstance(context, RedisClient):
        context.client.close()
