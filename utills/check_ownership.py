from db_dependency import db_dependency
from models import Artists, Document, DocumentsEpisodes


async def is_document_owned_by_artist(
        db: db_dependency,
        artist_id: int,
        document_id: int,
) -> bool:
    artist = db.query(Artists).where(
        Artists.Id == artist_id
    ).first()
    document = db.query(Document).where(Document.Id == document_id).first()
    if document and artist:
        return True if document.Owner == artist.Id else False
    return False


async def is_episode_owned_by_artist(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
) -> bool:
    artist = db.query(Artists).where(
        Artists.Id == artist_id
    ).first()

    episode, document = db.query(DocumentsEpisodes, Document).join(
        Document
    ).where(
        DocumentsEpisodes.Id == episode_id
    ).first()

    if artist and episode and document and episode.DocumentId == document.Id:
        return True if document.Owner == artist.Id else False
    return False
