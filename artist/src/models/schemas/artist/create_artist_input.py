from pydantic import BaseModel

class CreateArtistInput(BaseModel):
    name: str
    description: str