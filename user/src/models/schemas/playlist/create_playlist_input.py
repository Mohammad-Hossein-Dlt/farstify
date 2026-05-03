from pydantic import BaseModel

class CreatePlaylistInput(BaseModel):
    user_id: str
    title: str
    description: str | None = None
    public: bool = False