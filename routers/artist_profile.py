from access_token import optional_user_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, status
from constants import ContentTypes, OrderBy
from utills.check_follow import artist_follow
from actions.artist_actions import (
    fetch_profile,
    best_documents,
    best_episodes,
    fetch_all_artist_documents,
    fetch_artist_appears_on_documents,
    fetch_artist_appears_on_episodes, ArtistDocumentOrder,
)

router = APIRouter(prefix="/artist_profile", tags=["Artist-Profile"])


@router.get("/profile", status_code=status.HTTP_200_OK)
async def fetch_user_profile(
        db: db_dependency,
        artist_id: int,
        access_token: optional_user_token_dependency,
):
    artist_profile, artist_id = await fetch_profile(db, artist_id)

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


@router.get("/posts_all", status_code=status.HTTP_200_OK)
async def fetch_documents(
        db: db_dependency,
        artist_id: int,
        sort: ArtistDocumentOrder,
        singles: bool,
        limit: int,
        page: int,
        order_by: OrderBy,
        from_type: ContentTypes | None = None,
):
    return await fetch_all_artist_documents(
        db=db,
        artist_id=artist_id,
        sort=sort,
        singles=singles,
        limit=limit,
        page=page,
        order_by=order_by,
        from_type=from_type,
    )


@router.get("/contributed-posts", status_code=status.HTTP_200_OK)
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


@router.get("/contributed-episodes", status_code=status.HTTP_200_OK)
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
