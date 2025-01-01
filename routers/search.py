import models
from fastapi import APIRouter, status

from actions.episode_actions import get_episode_short_info
from db_dependency import db_dependency
from actions.artist_short_info_actions import get_artist_short_info
from actions.document_actions import get_document_short_info
from actions.playlist_actions import get_playlist_short_info

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/pre_search", status_code=status.HTTP_200_OK)
async def pre_search(
        db: db_dependency,
        limit: int,
        username: str,
):
    search = db.query(models.Artists.Name.label("result")).where(models.Artists.Name.contains(username)).union(
        db.query(models.Document.Name.label("result")).where(
            models.Document.Name.contains(username)
        ),
        db.query(models.PlayList.Title.label("result")).where(
            models.PlayList.Title.contains(username)
        ),
    ).limit(limit).all()

    result = [i.result for i in search]

    return result


@router.get("/document_search", status_code=status.HTTP_200_OK)
async def document_search(
        db: db_dependency,
        limit: int,
        page: int,
        name: str,
):
    search = db.query(models.Document).where(
        models.Document.Name.contains(name)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    result = [await get_document_short_info(db, document) for document in search]

    return result


@router.get("/episode_search", status_code=status.HTTP_200_OK)
async def document_search(
        db: db_dependency,
        limit: int,
        page: int,
        name: str,
):
    search = db.query(
        models.DocumentsEpisodes,
        models.Document
    ).join(
        models.Document,
    ).where(
        models.DocumentsEpisodes.Title.contains(name)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    result = [await get_episode_short_info(db, episode, document) for episode, document in search]

    return result


@router.get("/artist_search", status_code=status.HTTP_200_OK)
async def artist_search(
        db: db_dependency,
        name: str,
        limit: int,
        page: int,
):
    search = db.query(models.Artists).where(
        models.Artists.Name.contains(name)
    ).limit(limit).offset(limit * page).all()

    result = [get_artist_short_info(artist) for artist in search]

    return result


@router.get("/playlist_search", status_code=status.HTTP_200_OK)
async def playlist_search(
        db: db_dependency,
        limit: int,
        page: int,
        name: str,
):
    search = db.query(models.PlayList).where(
        models.PlayList.Title.contains(name)
    ).limit(limit).offset(limit * page).all()

    result = [await get_playlist_short_info(db, playlist) for playlist in search]

    return result
