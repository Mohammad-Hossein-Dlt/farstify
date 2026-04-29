from src.domain.enums import Environment
from src.infra.schemas.converter.converter_params import ConverterParams
from src.infra.schemas.broker.rabbitmq import RabbitParams
from src.infra.schemas.storage.minio_client import MinioParams
from src.infra.schemas.database.mongodb import MongodbParams
from src.infra.schemas.database.redis import RedisParams
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    
    ENVIRONMENT: Environment
    
    CONVERTER_PARAMS: ConverterParams
    RABBITMQ: RabbitParams
    MINIO: MinioParams
    MONGODB: MongodbParams
    REDIS: RedisParams
    
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=[
            f".env.{os.getenv("ENVIRONMENT", "dev")}",
            f"../.env.{os.getenv("ENVIRONMENT", "dev")}",
        ],
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings: Settings = Settings()
