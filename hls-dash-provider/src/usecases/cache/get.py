from src.repo.interface.Icache import ICacheRepo

class GetCache:
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
    ):
        
        self.cache_repo = cache_repo

    async def execute(
        self,
        cache_id: str,
    ) -> dict | str:
        
        return self.cache_repo.get(cache_id)