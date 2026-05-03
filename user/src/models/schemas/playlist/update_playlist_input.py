from pydantic import BaseModel

class UpdatePlaylistInput(BaseModel):
    id: str
    title: str | None = None
    description: str | None = None
    public: bool | None = None