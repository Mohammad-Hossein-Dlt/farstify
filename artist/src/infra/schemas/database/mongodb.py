from .database_params import BaseDatabaseParams
from .database_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from pymongo.asynchronous.mongo_client import AsyncMongoClient

class MongodbParams(BaseDatabaseParams):
    pass


class MongodbClient(BaseDatabaseClient, BaseModel):
    params: MongodbParams
    client: AsyncMongoClient

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_dependency(self):
        yield self.client
