from pydantic import BaseModel, ConfigDict

class BaseDatabaseParams(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
