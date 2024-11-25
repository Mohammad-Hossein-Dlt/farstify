from actions_functions.listened import get_listened_times
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List
import models
from sqlalchemy import and_
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path
from utills.get_duration import get_formatted_duration
from actions.link_actions import LinkData
from actions.categories_actions import get_child_to_parent
from actions.artist_short_info_actions import ArtistShortInfo, get_artist_short_info


class DocumentInfo(BaseModel):
    Id: int | None = None
    Artist: ArtistShortInfo | None = None
    Name: str | None = None
    ImageUrl: str | None = None
    Description: str | None = None
    ContentType: str | None = None
    Duration: str | None = None
    CreationDate: str | None = None
    Single: bool | None = None
    Active: bool | None = None
    EpisodesNumber: int | None = None
    ListenedTimes: int | None = None
    Saves: int | None = None
    Likes: int | None = None
    Contributors: List = []
    Links: List = []
    Categories: List = []
    Labels: List[LinkData] = []
    # -----------------------------------
    Followed: bool = False


class DocumentShortInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ImageUrl: str | None = None
    ContentType: str | None = None
    Description: str | None = None
    ArtistName: str | None = None
    ArtistProfileImageUrl: str | None = None
    CreationDate: str | None = None
    Single: bool | None = None


async def get_document_full_info(
        db: db_dependency,
        document: models.Document,
        artist: models.Artists | None = None,
) -> DocumentInfo:
    if not artist:
        artist = db.query(models.Artists).where(models.Artists.Id == document.Owner).first()

    data = DocumentInfo()
    data.Id = document.Id
    data.Artist = get_artist_short_info(artist)
    data.Name = document.Name
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    ) if document.MainImage else None
    data.Description = document.Description
    data.Active = document.Active
    data.ContentType = document.ContentType
    data.EpisodesNumber = db.query(models.DocumentsEpisodes).where(
        models.DocumentsEpisodes.DocumentId == document.Id).count()
    data.ListenedTimes = await get_listened_times(db=db, document_id=document.Id)
    data.Saves = db.query(models.UserFollowing).where(models.UserFollowing.DocumentId == document.Id).count()
    data.Likes = db.query(models.UserLikes).where(models.UserLikes.DocumentId == document.Id).count()
    # data.Likes = get_likes(documentId=document.Id)
    data.CreationDate = document.CreationDate

    durations = db.query(models.DocumentsEpisodes.Duration).where(
        models.DocumentsEpisodes.DocumentId == document.Id
    ).all()

    duration = sum([duration[0] for duration in durations])
    data.Duration = get_formatted_duration(duration)
    contributors = db.query(models.Artists).select_from(
        models.Contributors,
    ).where(
        and_(
            models.Contributors.ArtistId == models.Artists.Id,
            models.Contributors.DocumentId == document.Id,
        )
    ).all()

    data.Contributors = [get_artist_short_info(artist=art) for art in contributors]

    links = db.query(models.DocumentsLinks).where(
        models.DocumentsLinks.DocumentId == document.Id
    ).order_by(
        models.DocumentsLinks.OrderBy.is_(None),
        models.DocumentsLinks.OrderBy.asc()
    ).all()

    data.Links = [LinkData(Title=link.Title, Link=link.Link) for link in links]

    category = db.query(models.DocumentsCategories).where(
        models.DocumentsCategories.DocumentId == document.Id
    ).order_by(
        models.DocumentsCategories.OrderBy.is_(None),
        models.DocumentsCategories.OrderBy.asc()
    ).all()

    data.Categories = [await get_child_to_parent(db, x.CategoryId, contains_self=True) for x in category]

    labels = db.query(models.DocumentsLabels).where(
        models.DocumentsLabels.DocumentId == document.Id).all()

    data.Labels = [x.Title for x in labels]

    return data


async def get_document_short_info(
        db: db_dependency,
        document: models.Document,
        artist: models.Artists | None = None,
) -> DocumentShortInfo:
    if not artist:
        artist = db.query(models.Artists).where(models.Artists.Id == document.Owner).first()

    data = DocumentShortInfo()
    data.Id = document.Id
    data.Name = document.Name
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    ) if document.MainImage else None

    data.Description = document.Description

    data.ContentType = document.ContentType

    data.ArtistName = artist.Name

    data.CreationDate = document.CreationDate

    return data
