from .app_context import AppContext
from src.infra.settings.settings import settings
from src.infra.bootstrap.broker import init_broker_client, terminate_broker_client
from src.infra.bootstrap.storage import init_storage_client, terminate_storage_client
from src.infra.bootstrap.database import init_database_client, terminate_database_client
from src.infra.bootstrap.cache_database import init_cache_client, terminate_cache_client
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):
        
        AppContext.environment = settings.ENVIRONMENT
        AppContext.converter_params = settings.CONVERTER_PARAMS
        AppContext.broker_client = init_broker_client(settings.RABBITMQ)
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        AppContext.storage_client = await init_storage_client(settings.MINIO)
        AppContext.db_client = await init_database_client(settings.MONGODB)
        AppContext.cache_client = await init_cache_client(settings.REDIS)
        
        await AppContext.broker_client.broker.connect()
        
        AppContext.http_client = ClientSession()

    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await terminate_broker_client(AppContext.broker_client)
        await terminate_storage_client(AppContext.storage_client)
        await terminate_database_client(AppContext.db_client)
        await terminate_cache_client(AppContext.cache_client)
        await AppContext.http_client.close()

AppContextManager.init_context()