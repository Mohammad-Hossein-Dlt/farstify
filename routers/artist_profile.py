import models
from access_token import optional_user_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from constants import OrderBy
from utills.check_follow import artist_follow
from actions.artist_actions import (
    best_documents,
    best_episodes,
    fetch_all_artist_documents,
    fetch_artist_appears_on_documents,
    fetch_artist_appears_on_episodes,
    ArtistDocumentsSortBy,
    get_artist_personal_info,
    get_artist_profile_info,
)

router = APIRouter(prefix="/artist_profile", tags=["Artist-Profile"])


@router.get("/short_info", status_code=status.HTTP_200_OK)
async def fetch_user_profile(
        db: db_dependency,
        artist_id: int,
        access_token: optional_user_token_dependency,
):
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        raise HTTPException(404, "artist not found!")

    artist_profile = await get_artist_profile_info(db, artist)

    if access_token.permission:
        artist_profile.Followed = await artist_follow(db=db, user_id=access_token.user_id, artist_id=artist_id)

    return artist_profile


@router.get("/full_info", status_code=status.HTTP_200_OK)
async def fetch_user_profile(
        db: db_dependency,
        artist_id: int,
        access_token: optional_user_token_dependency,
):
    artist = db.query(
        models.Artists
    ).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, "artist not found!")

    artist_profile = await get_artist_personal_info(db, artist)

    if access_token.permission:
        artist_profile.Followed = await artist_follow(db=db, user_id=access_token.user_id, artist_id=artist_id)

    return artist_profile


@router.get("/best_documents", status_code=status.HTTP_200_OK)
async def my_best_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,

):
    return await best_documents(db, artist_id, limit, page)


@router.get("/best_episodes", status_code=status.HTTP_200_OK)
async def my_best_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):
    return await best_episodes(db, artist_id, limit, page)


@router.get("/all_documents", status_code=status.HTTP_200_OK)
async def fetch_documents(
        db: db_dependency,
        artist_id: int,
        sort: ArtistDocumentsSortBy,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await fetch_all_artist_documents(
        db=db,
        artist_id=artist_id,
        sort=sort,
        limit=limit,
        page=page,
        order_by=order_by,
    )


@router.get("/contributed_documents", status_code=status.HTTP_200_OK)
async def fetch_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await fetch_artist_appears_on_documents(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
        order_by=order_by,
    )


@router.get("/contributed_episodes", status_code=status.HTTP_200_OK)
async def fetch_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await fetch_artist_appears_on_episodes(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
        order_by=order_by,
    )
