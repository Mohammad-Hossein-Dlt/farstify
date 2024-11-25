from fastapi import HTTPException
from db_dependency import db_dependency
import models


def add_listened(
        db: db_dependency,
        artist_id: int,
        user_id: int,
        document_id: int,
        episode_id: int,
):
    listened = models.ListenedHistory
    listened.ArtistsId = artist_id
    listened.UserId = user_id
    listened.DocumentId = document_id
    listened.EpisodeId = episode_id

    db.add(listened)

    db.commit()


# async def get_artists_listened_documents(
#         db: db_dependency,
#         artist: models.Artists,
#         limit: int,
#         page: int,
# ) -> List[DocumentShortInfo]:
#     sub = db.query(
#         models.Document, func.max(models.ListenedHistory.DocumentId).label("max_listened")
#     ).outerjoin(
#         models.ListenedHistory
#     ).group_by(
#         models.Document.Id
#     ).subquery()
#
#     docs = db.query(models.Document).join(
#         sub,
#         models.Document.Id == sub.c.Id
#     ).where(
#         models.Document.Owner == artist.Id
#     ).order_by(
#         desc(sub.c.max_listened)
#     ).limit(limit).offset(limit * page).all()
#
#     return [await get_document_short_info(db, i, artist) for i in docs]


# async def get_artists_listened_episodes(
#         db: db_dependency,
#         artist: models.Artists,
#         limit: int,
#         page: int,
# ) -> List[EpisodeShortInfo]:
#     sub = db.query(
#         models.DocumentsEpisodes, func.max(models.ListenedHistory.DocumentId).label("max_listened")
#     ).outerjoin(
#         models.ListenedHistory
#     ).group_by(
#         models.DocumentsEpisodes.Id
#     ).subquery()
#
#     episodes = db.query(models.DocumentsEpisodes).join(
#         sub,
#         models.DocumentsEpisodes.Id == sub.c.Id
#     ).join(
#         models.Document,
#         models.Document.Owner == artist.Id,
#     ).order_by(
#         desc(sub.c.max_listened)
#     ).limit(limit).offset(limit * page).all()
#
#     return [await get_episode_short_info(db, i, artist) for i in episodes]


async def get_listened_times(
        db: db_dependency,
        artist_id: int | None = None,
        episode_id: int | None = None,
        document_id: int | None = None
) -> int:
    params = [artist_id, episode_id, document_id]
    given_params_num = sum(p is not None for p in params)
    if given_params_num != 1:
        raise HTTPException(403, "only one entity must be given")

    result = 0
    if artist_id:
        result = db.query(models.ListenedHistory).where(models.ListenedHistory.ArtistsId == artist_id).count()

    if episode_id:
        result = db.query(models.ListenedHistory).where(models.ListenedHistory.EpisodeId == episode_id).count()

    if document_id:
        result = db.query(models.ListenedHistory).where(models.ListenedHistory.DocumentId == document_id).count()

    return result
