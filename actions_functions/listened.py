from fastapi import HTTPException
from db_dependency import db_dependency
import models
from sqlalchemy import func


def add_listened(
        db: db_dependency,
        user_id: int,
        episode_id: int,
):
    listened = models.ListenedHistory()
    listened.UserId = user_id
    listened.EpisodeId = episode_id

    db.add(listened)

    db.commit()


async def get_listened_times(
        db: db_dependency,
        artist_id: int | None = None,
        document_id: int | None = None,
        episode_id: int | None = None,
) -> int:
    params = [artist_id, episode_id, document_id]
    given_params_num = sum(p is not None for p in params)
    if given_params_num != 1:
        raise HTTPException(403, "only one entity must be given")

    result = 0
    if artist_id:

        result = db.query(
            func.count(models.ListenedHistory.Id)
        ).join(
            models.DocumentsEpisodes,
            models.ListenedHistory.EpisodeId == models.DocumentsEpisodes.Id
        ).join(
            models.Document,
            models.DocumentsEpisodes.DocumentId == models.Document.Id,
        ).join(
            models.DocumentsOwners,
            models.Document.Id == models.DocumentsOwners.DocumentId,
        ).filter(
            models.DocumentsOwners.ArtistId == artist_id
        ).scalar()

    if episode_id:
        result = db.query(models.ListenedHistory).where(models.ListenedHistory.EpisodeId == episode_id).count()

    if document_id:

        result = db.query(
            func.count(models.ListenedHistory.Id)
        ).join(
            models.DocumentsEpisodes,
            models.ListenedHistory.EpisodeId == models.DocumentsEpisodes.Id
        ).join(
            models.Document,
            models.DocumentsEpisodes.DocumentId == models.Document.Id,
        ).filter(
            models.Document.Id == document_id,
        ).scalar()

    return result
