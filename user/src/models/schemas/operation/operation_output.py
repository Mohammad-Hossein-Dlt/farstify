from pydantic import BaseModel, ConfigDict, field_serializer

class OperationOutput(BaseModel):
    id: int | str | None = None
    request: str
    status: bool
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
    )
    
    @field_serializer("id")
    def id_serializer(
        self,
        var,
    ):
        try:
            return int(var)
        except:
            pass
        
        return str(var) if var else None