from pydantic import BaseModel

class CreateImageInput(BaseModel):
    artist_id: str
    is_main: bool = False