from src.repo.interface.Istorage_repo import IStorageRepo
from minio import Minio
import minio.error
from minio.deleteobjects import DeleteObject
import tempfile
from urllib3 import BaseHTTPResponse, HTTPHeaderDict
import os

class MinioRepo(IStorageRepo):
    
    def __init__(
        self,
        client: Minio,
        bucket_name: str,
    ):
        
        self.client = client
        self.bucket_name = bucket_name
    
    async def setup_bucket(
        self,
        bucket_name: str,
    ) -> bool:
    
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            
    async def path_objects(
        self,
        path: str | None = None,
        bucket_name: str | None = None,
    ) -> list[str | None]:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            objects = self.client.list_objects(
                bucket_name=bucket_name,
                prefix=path,
                recursive=True,
            )
            return [ i.object_name for i in objects]
        except minio.error.S3Error as e:
            print(e)
            return []
            
    async def upload_object(
        self,
        file: tempfile.SpooledTemporaryFile | str,
        object_name: str,
        file_size: int | None = None,
        content_type: str | None = None,
        bucket_name: str | None = None,
    ) -> bool:
    
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            if isinstance(file, tempfile.SpooledTemporaryFile):
                if file_size and content_type:
                    self.client.put_object(bucket_name, object_name, file, file_size, content_type)
                else:
                    return False
            elif isinstance(file, str):
                self.client.fput_object(bucket_name, object_name, file)

            return True 
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
        
    async def get_object_stat(
        self,
        object_name: str,
        bucket_name: str | None = None,
    ) -> HTTPHeaderDict | None:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            return self.client.stat_object(bucket_name, object_name).metadata
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return None
                        
    async def get_object(
        self,
        object_name: str,
        bucket_name: str | None = None,
    ) -> BaseHTTPResponse:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            return self.client.get_object(bucket_name, object_name)
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
                
    async def get_url(
        self,
        object_name: str,
        bucket_name: str | None = None,
    ) -> str:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            return self.client.get_presigned_url("GET", bucket_name, object_name)
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
        
    async def delete_object(
        self,
        object_name: str,
        bucket_name: str | None = None,
    ) -> bool:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            self.client.remove_object(bucket_name, object_name)
            return True 
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
    
    async def upload_objects(
        self,
        path: str,
        base_object_name: str,
        bucket_name: str | None = None,
    ) -> bool:
        
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    local_file = os.path.join(root, file)            
                    object_name = os.path.relpath(local_file, path)
                    await self.upload_object(
                        local_file,
                        base_object_name + object_name,
                        bucket_name=bucket_name,
                    )
            
            return True
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
        
    async def clean_dir(
        self,
        path: str | None = None,
        bucket_name: str | None = None,
    ) -> bool:
        
        try:
            bucket_name = bucket_name or self.bucket_name
            await self.setup_bucket(bucket_name)
            objects_list = await self.path_objects(path, bucket_name)
            delete_list = [ DeleteObject(name=i) for i in objects_list ]
            if delete_list:
                errors = self.client.remove_objects(bucket_name, delete_list)
                for err in errors:
                    print(err)            

            return True
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False
        
    async def delete_objects(
        self,
        path: str,
        bucket_name: str | None = None,
    ) -> bool:
        
        try:
            clean = await self.clean_dir(path, bucket_name)
            if clean:
                clean = await self.delete_object(path, bucket_name)

            return clean
        except minio.error.S3Error as e:
            print(f"Error: {e}")
            return False