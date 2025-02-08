import models
from access_token import optional_user_token_dependency
from actions.raw_artist_info_actions import get_raw_artist_info
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from constants import OrderBy
from utills.check_follow import artist_follow
from actions.artist_actions import (
    get_best_documents,
    get_best_episodes,
    get_all_artist_documents,
    get_artist_appears_on_documents,
    get_artist_appears_on_episodes,
    ArtistDocumentsSortBy,
    get_artist_profile_info,
    get_artist_page_info,
)

router = APIRouter(prefix="/artist", tags=["General-Artist"])


@router.get("/fetch_all_artists", status_code=status.HTTP_201_CREATED)
async def add_artist(
        db: db_dependency,
        limit: int,
        page: int,
):
    artists = db.query(
        models.Artists
    ).order_by(
        models.Artists.Id.asc()
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    return [
        get_raw_artist_info(i) for i in artists
    ]


@router.get("/raw", status_code=status.HTTP_200_OK)
async def fetch_raw_artist(
        db: db_dependency,
        artist_id: int,
):
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        raise HTTPException(404, "admin not found!")

    artist_profile = get_raw_artist_info(artist)

    return artist_profile


@router.get("/page", status_code=status.HTTP_200_OK)
async def fetch_artist_page(
        db: db_dependency,
        artist_id: int,
        access_token: optional_user_token_dependency,
):
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        raise HTTPException(404, "admin not found!")

    artist_profile = await get_artist_page_info(db, artist)

    if access_token.permission:
        artist_profile.Followed = await artist_follow(db=db, user_id=access_token.user_id, artist_id=artist_id)

    return artist_profile


@router.get("/profile", status_code=status.HTTP_200_OK)
async def fetch_artist_profile(
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
        raise HTTPException(404, "admin not found!")

    artist_profile = await get_artist_profile_info(db, artist)

    if access_token.permission:
        artist_profile.Followed = await artist_follow(db=db, user_id=access_token.user_id, artist_id=artist_id)

    return artist_profile


@router.get("/best_documents", status_code=status.HTTP_200_OK)
async def fetch_best_artist_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,

):
    return await get_best_documents(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
    )


@router.get("/best_episodes", status_code=status.HTTP_200_OK)
async def fetch_best_artist_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):
    return await get_best_episodes(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
    )


@router.get("/all_documents", status_code=status.HTTP_200_OK)
async def fetch_all_artist_documents(
        db: db_dependency,
        artist_id: int,
        sort: ArtistDocumentsSortBy,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await get_all_artist_documents(
        db=db,
        artist_id=artist_id,
        sort=sort,
        limit=limit,
        page=page,
        order_by=order_by,
    )


@router.get("/contributed_documents", status_code=status.HTTP_200_OK)
async def fetch_artist_contributed_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await get_artist_appears_on_documents(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
        order_by=order_by,
    )


@router.get("/contributed_episodes", status_code=status.HTTP_200_OK)
async def fetch_artist_contributed_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    return await get_artist_appears_on_episodes(
        db=db,
        artist_id=artist_id,
        limit=limit,
        page=page,
        order_by=order_by,
    )
