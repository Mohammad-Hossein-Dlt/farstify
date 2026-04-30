from pydantic import BaseModel

class CreateEpisodeInput(BaseModel):
    document_id: int | str
    title: str
    description: str | None = None
    active: bool = False