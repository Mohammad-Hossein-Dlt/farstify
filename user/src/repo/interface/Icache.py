from abc import ABC, abstractmethod

class ICacheRepo(ABC):
    
    @abstractmethod
    def save(
        cache_id: str,
        data: dict | str,
        ttl: int,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def incrby(
        cache_id: str,
        amount: int,
    ) -> int:
        
        raise NotImplementedError
    
    @abstractmethod
    def decrby(
        cache_id: str,
        amount: int,
    ) -> int:
        
        raise NotImplementedError
    
    @abstractmethod
    def get(
        cache_id: str,
    ) -> dict | str | None:
        
        raise NotImplementedError
    
    @abstractmethod
    def delete(
        cache_id: str,
    ) -> bool:
        
        raise NotImplementedError
