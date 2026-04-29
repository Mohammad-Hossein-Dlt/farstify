from pydantic import BaseModel

class UpdateArtistInput(BaseModel):
    id: int | str
    name: str | None = None
    description: str | None = None