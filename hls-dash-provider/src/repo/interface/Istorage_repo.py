from abc import ABC, abstractmethod
import tempfile
from urllib3 import BaseHTTPResponse, HTTPHeaderDict 

class IStorageRepo(ABC):
        
    @abstractmethod
    async def setup_bucket(
        bucket_name: str,
    ) -> bool:
    
        raise NotImplementedError

    @abstractmethod
    async def path_objects(
        path: str,
        bucket_name: str | None = None,
    ) -> list[str]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def upload_object(
        file: tempfile.SpooledTemporaryFile | str,
        object_name: str,
        file_size: int | None = None,
        content_type: str | None = None,
        bucket_name: str | None = None,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_object_stat(
        object_name: str,
        bucket_name: str | None = None,
    ) -> HTTPHeaderDict | None:
    
        raise NotImplementedError
        
    @abstractmethod
    async def get_object(
        object_name: str,
        bucket_name: str | None = None,
    ) -> BaseHTTPResponse:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_url(
        object_name: str,
        bucket_name: str | None = None,
    ) -> str:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_object(
        object_name: str,
        bucket_name: str | None = None,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def upload_objects(
        path: str,
        base_object_name: str,
        bucket_name: str | None = None,
    ) -> bool:
        
        raise NotImplementedError
    
    @abstractmethod
    async def clean_dir(
        path: str | None = None,
        bucket_name: str | None = None,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_objects(
        path: str,
        bucket_name: str | None = None,
    ) -> bool:
    
        raise NotImplementedError