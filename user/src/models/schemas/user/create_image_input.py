from pydantic import BaseModel

class CreateImageInput(BaseModel):
    user_id: str
    is_main: bool = False