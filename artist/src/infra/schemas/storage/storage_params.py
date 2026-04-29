from pydantic import BaseModel, ConfigDict

class BaseStorageParams(BaseModel):
    host: str
    access_key: str
    secret_key: str
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
