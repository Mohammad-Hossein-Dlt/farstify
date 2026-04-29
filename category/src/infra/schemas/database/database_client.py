from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient

class BaseDatabaseClient(ABC):

    @abstractmethod
    def get_dependency(self) -> Session | AsyncMongoClient:
        raise NotImplementedError