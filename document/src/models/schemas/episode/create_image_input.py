from pydantic import BaseModel

class CreateImageInput(BaseModel):
    episode_id: str
    is_main: bool = False