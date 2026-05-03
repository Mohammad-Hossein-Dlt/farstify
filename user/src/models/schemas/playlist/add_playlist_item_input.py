from pydantic import BaseModel

class AddPlaylistItemInput(BaseModel):
    playlist_id: str
    episode_id: str