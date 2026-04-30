from pydantic import BaseModel

class UpdateEpisodeInput(BaseModel):
    id: int | str
    title: str | None = None
    description: str | None = None
    active: bool | None = None