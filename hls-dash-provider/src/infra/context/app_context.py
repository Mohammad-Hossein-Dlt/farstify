from typing import ClassVar
from src.domain.enums import Environment
from src.infra.schemas.converter.converter_params import ConverterParams
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.infra.schemas.storage.minio_client import MinioClient
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.schemas.database.redis import RedisClient
from aiohttp import ClientSession

class AppContext(type):
        
    environment: ClassVar[Environment] = None
    converter_params: ClassVar[ConverterParams] = None
    broker_client: ClassVar[RabbitClient] = None
    storage_client: ClassVar[MinioClient] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    cache_client: ClassVar[RedisClient] = None
    http_client: ClassVar[ClientSession] = None