from src.domain.schemas.playlist.playlist_item_model import PlaylistItemModel
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class PlaylistItemCollection(PlaylistItemModel, Document):

    id: PydanticObjectId = None
    playlist_id: PydanticObjectId
    episode_id: PydanticObjectId
    order: int | None = None
    
    class Settings:
        name = "Playlist_Item"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)