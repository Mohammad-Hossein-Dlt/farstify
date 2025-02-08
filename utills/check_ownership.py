from db_dependency import db_dependency
from models import Artists, Document, DocumentsEpisodes, DocumentsOwners

from sqlalchemy import and_


async def is_document_owned_by_artist(
        db: db_dependency,
        artist_id: int,
        document_id: int,
) -> bool:
    # admin = db.query(Artists).where(
    #     Artists.Id == artist_id
    # ).first()
    ownership = db.query(DocumentsOwners).where(
        and_(
            DocumentsOwners.ArtistId == artist_id,
            DocumentsOwners.DocumentId == document_id,
        )
    ).first()
    if ownership:
        return True
    return False


async def is_episode_owned_by_artist(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
) -> bool:
    # admin = db.query(Artists).where(
    #     Artists.Id == artist_id
    # ).first()

    episode, document = db.query(DocumentsEpisodes, Document).join(
        Document
    ).where(
        DocumentsEpisodes.Id == episode_id
    ).first()

    ownership = db.query(DocumentsOwners).where(
        and_(
            DocumentsOwners.ArtistId == artist_id,
            DocumentsOwners.DocumentId == document.Id,
        )
    ).first()

    if ownership:
        return True
    return False
