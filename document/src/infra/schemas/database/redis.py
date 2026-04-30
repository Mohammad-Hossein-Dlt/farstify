from .database_params import BaseDatabaseParams
from .database_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from redis import Redis

class RedisParams(BaseDatabaseParams):
    username: str | None = None
    db_name: str | None = None

class RedisClient(BaseDatabaseClient, BaseModel):
    params: RedisParams
    client: Redis

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_dependency(self):
        yield self.client
