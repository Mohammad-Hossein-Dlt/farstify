import models
from passlib.context import CryptContext
from access_token import user_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status
from actions.response_model import ResponseMessage
from sqlalchemy import and_, asc, desc
from constants import OrderBy
from actions.raw_artist_info_actions import get_raw_artist_info
from actions.document_actions import get_document_short_info
from actions.playlist_actions import get_playlist_short_info

router = APIRouter(prefix="/user/follow", tags=["User-Follow"])

@router.put("/follow_action", status_code=status.HTTP_200_OK)
async def follow(
        db: db_dependency,
        access_token: user_token_dependency,
        artist_id: int | None = None,
        document_id: int | None = None,
        play_list_id: int | None = None,
):
    params = [artist_id, document_id, play_list_id]

    given_params_num = sum(p is not None for p in params)

    if given_params_num != 1:
        raise HTTPException(403, "only one entity must be given")

    check = db.query(
        models.UserFollowing
    ).where(
        and_(
            models.UserFollowing.ArtistId == artist_id,
            models.UserFollowing.DocumentId == document_id,
            models.UserFollowing.PlayListId == play_list_id,
        ),
    ).first()

    if check:
        db.delete(check)
        db.commit()
        return ResponseMessage(error=False, message="Ok. your following has been removed.")

    new_follow = models.UserFollowing()
    new_follow.UserId = access_token.user_id

    if artist_id:
        new_follow.ArtistId = artist_id

    if document_id:
        new_follow.DocumentId = document_id

    if play_list_id:
        new_follow.PlayListId = play_list_id

    db.add(new_follow)
    db.commit()

    return ResponseMessage(error=False, message="Ok. your following has added.")


@router.get("/fetch_following", status_code=status.HTTP_200_OK)
async def fetch_following(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []

    docs = db.query(
        models.UserFollowing,
        models.Artists,
        models.Document,
        models.PlayList
    ).join(
        models.Artists,
        models.UserFollowing.ArtistId == models.Artists.Id,
        isouter=True,
    ).join(
        models.Document,
        models.UserFollowing.DocumentId == models.Document.Id,
        isouter=True,
    ).join(
        models.PlayList,
        models.UserFollowing.PlayListId == models.PlayList.Id,
        isouter=True,
    ).filter(
        models.UserFollowing.UserId == access_token.user_id
    ).order_by(
        desc(models.UserFollowing.Id) if order_by is OrderBy.desc else asc(models.UserFollowing.Id)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for _, artist, document, playlist in docs:
        if artist:
            result.append({"type": "admin", "data": get_raw_artist_info(artist)})

        if document:
            result.append({"type": "document", "data": await get_document_short_info(db=db, document=document)})

        if playlist:
            result.append({"type": "playlistId", "data": await get_playlist_short_info(db, playlist)})

    return result
