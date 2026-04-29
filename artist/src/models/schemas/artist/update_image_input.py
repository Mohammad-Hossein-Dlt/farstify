from pydantic import BaseModel

class UpdateImageInput(BaseModel):
    id: str
    is_main: bool = False