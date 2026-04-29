from src.repo.interface.Icache import ICacheRepo

class SaveCache:
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
    ):
        
        self.cache_repo = cache_repo

    async def execute(
        self,
        cache_id: str,
        data: dict | str | None = None,
    ) -> dict | str:
        
        cached = self.cache_repo.get(cache_id)
        
        if isinstance(cached, dict):
            data.update(cached)
            # data = dict(sorted(data.items(), key=lambda x: x[0]))
        
        return self.cache_repo.save(
            cache_id,
            data,
            60 * 5,
        )
        