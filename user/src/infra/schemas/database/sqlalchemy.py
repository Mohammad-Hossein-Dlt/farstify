from .database_params import BaseDatabaseParams
from .database_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

class SqlalchemyParams(BaseDatabaseParams):
    pass

class SqlalchemyClient(BaseDatabaseClient, BaseModel):
    params: SqlalchemyParams
    engine: Engine
    client: sessionmaker

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    
    def get_dependency(self):
        session: Session = self.client()
        try:
            yield session
        finally:
            session.close()