from fastapi import HTTPException

from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List
import models
from actions.user_actions import SingleUserProfileData, user_profile_data
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path
from utills.get_duration import get_formatted_duration


class PlayListFullInfo(BaseModel):
    Id: int | None = None
    Owner: SingleUserProfileData | None = None
    Images: List = []
    Title: str | None = None
    Description: str | None = None
    Public: bool | None = None
    CreationDate: str | None = None
    EpisodesNumber: int | None = None
    Saves: int | None = None
    Duration: str | None = None
    # -----------------------------------
    Followed: bool = False


class PlayListShortInfo(BaseModel):
    Id: int | None = None
    User: SingleUserProfileData | None = None
    Images: List = []
    Title: str | None = None
    CreationDate: str | None = None


async def get_playlist_full_info(
        db: db_dependency,
        playlist: models.PlayList,
) -> PlayListFullInfo:

    data = PlayListFullInfo()

    user = db.query(
        models.Users
    ).where(
        models.Users.Id == playlist.OwnerUser
    ).first()

    if not user:
        raise HTTPException(404, "user not found!")

    playlist_items = db.query(
        models.PlayListRepository,
        models.DocumentsEpisodes,
        models.Document,
    ).join(
        models.DocumentsEpisodes,
        models.PlayListRepository.EpisodesId == models.DocumentsEpisodes.Id,
        isouter=True
    ).join(
        models.Document,
        models.PlayListRepository.DocumentId == models.Document.Id,
        isouter=True
    ).where(
        models.PlayListRepository.PlayListId == playlist.Id
    ).all()

    duration = 0
    images = []
    for _, episode, document in playlist_items:
        image_url = make_path(document.DirectoryName, document.MainImage, is_file=True)
        if not images.__contains__(image_url) or not len(images) >= 4:
            images.append(image_url)
        duration += episode.Duration

    data.Images = [
        encode_link(bucket_name=Buckets.DOCUMENT_BUCKET_NAME, path=image)
        for image in images
    ]

    data.Id = playlist.Id
    data.Owner = user_profile_data(user)
    data.Title = playlist.Title
    data.Description = playlist.Description
    data.Public = playlist.Public
    data.CreationDate = playlist.CreationDate
    data.EpisodesNumber = db.query(models.PlayListRepository).where(
        models.PlayListRepository.PlayListId == playlist.Id
    ).count()
    data.Saves = db.query(models.UserFollowing).where(models.UserFollowing.PlayListId == playlist.Id).count()
    data.Duration = get_formatted_duration(duration)

    return data


async def get_playlist_short_info(
        db: db_dependency,
        playlist: models.PlayList,
) -> PlayListShortInfo:

    data = PlayListShortInfo()

    user = db.query(
        models.Users
    ).where(
        models.Users.Id == playlist.OwnerUser
    ).first()

    if not user:
        raise HTTPException(404, "user not found!")

    playlist_items = db.query(
        models.PlayListRepository,
        models.DocumentsEpisodes,
        models.Document,
    ).join(
        models.DocumentsEpisodes,
        models.PlayListRepository.EpisodesId == models.DocumentsEpisodes.Id,
        isouter=True
    ).join(
        models.Document,
        models.PlayListRepository.DocumentId == models.Document.Id,
        isouter=True
    ).where(
        models.PlayListRepository.PlayListId == playlist.Id
    ).order_by(
        models.PlayListRepository.Id.asc()
    ).all()

    duration = 0
    images = []
    for _, episode, document in playlist_items:
        image_url = make_path(document.DirectoryName, document.MainImage, is_file=True)
        if not images.__contains__(image_url) or not len(images) >= 4:
            images.append(image_url)
        duration += episode.Duration

    data.Images = [
        encode_link(bucket_name=Buckets.DOCUMENT_BUCKET_NAME, path=image)
        for image in images
    ]

    data.Id = playlist.Id
    data.User = user_profile_data(user)
    data.Title = playlist.Title
    data.CreationDate = playlist.CreationDate

    return data
