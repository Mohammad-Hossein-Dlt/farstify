from pydantic import BaseModel, ConfigDict

class BrokerParams(BaseModel):
    url: str
    exchange: str    
    queue: str    
    routing_key: str 

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
