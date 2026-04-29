from redis import Redis
from src.repo.interface.Icache import ICacheRepo
import json

class RedisCacheRepo(ICacheRepo):
    
    def __init__(
        self,
        redis_client: Redis,
    ):
        
        self.redis_client = redis_client
        
    def save(
        self,
        cache_id: str,
        data: dict | str,
        ttl: int,
    ) -> dict:
                
        self.redis_client.execute_command(
            "JSON.SET",
            cache_id,
            ".",
            json.dumps(data),
        )
                
        self.redis_client.expire(
            cache_id,
            ttl,
        )
                                                
        return data

    def incrby(
        self,
        cache_id: str,
        amount: int,
    ) -> dict | str | None:
        
        return self.redis_client.incrby(cache_id, amount)
                
    def decrby(
        self,
        cache_id: str,
        amount: int,
    ) -> dict | str | None:
        
        return self.redis_client.decrby(cache_id, amount)

    def get(
        self,
        cache_id: str,
    ) -> dict | str | None:
        
        try:

            cached = self.redis_client.execute_command(
                "JSON.GET",
                cache_id,
            )
            try:
                return json.loads(cached)
            except:
                if isinstance(cached, str):
                    return cached
        except:
            return None
        
    def delete(
        self,
        cache_id: str,
    ) -> bool | None:
        
        try:

            self.redis_client.unlink(cache_id)
            return True
        except:
            return False
