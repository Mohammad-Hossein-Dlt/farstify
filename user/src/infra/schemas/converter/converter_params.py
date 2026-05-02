from pydantic import BaseModel, ConfigDict

class ConverterParams(BaseModel):
    bitrate: int
    number: int
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
