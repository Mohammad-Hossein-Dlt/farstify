from abc import ABC, abstractmethod
from src.domain.enums import Format

class IBrokerService(ABC):
    
    @abstractmethod
    async def convert(
        object_name: str,
        format: Format,
    ) -> bool:
        
        raise NotImplementedError
    
    @abstractmethod
    async def create_stream_file(
        object_name: str,
        format: Format,
    ) -> bool:
        
        raise NotImplementedError