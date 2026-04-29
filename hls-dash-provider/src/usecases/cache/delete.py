from src.repo.interface.Icache import ICacheRepo

class DeleteCache:
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
    ):
        
        self.cache_repo = cache_repo

    async def execute(
        self,
        cache_id: str,
    ) -> bool:
        
        return self.cache_repo.delete(cache_id)