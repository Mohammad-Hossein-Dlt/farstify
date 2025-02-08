import pathlib
import uuid
from fastapi import UploadFile, File
from sqlalchemy import func
from actions.response_model import ResponseMessage
from actions_functions.listened import get_listened_times
from constants import ContentTypes, DocumentQualities
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List
import models
from utills.encode_link import encode_link
from storage import Buckets, storage, storage_delete_file
from utills.parse_null import pars_null
from utills.path_manager import make_path
from utills.get_duration import get_formatted_duration
from actions.categories_actions import get_child_to_parent
from actions.raw_artist_info_actions import RawArtistInfo, get_raw_artist_info


class DocumentFullInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ImageUrl: str | None = None
    Color: str | None = None
    Description: str | None = None
    ContentType: str | None = None
    Single: bool | None = None
    Active: bool | None = None
    CreationDate: str | None = None
    Duration: str | None = None
    EpisodesNumber: int | None = None
    ListenedTimes: int | None = None
    Saves: int | None = None
    Likes: int | None = None
    Artists: List[RawArtistInfo] | None = None
    Categories: List = []
    # -----------------------------------
    Followed: bool = False


class DocumentShortInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ImageUrl: str | None = None
    ContentType: str | None = None
    Description: str | None = None
    CreationDate: str | None = None
    Single: bool | None = None
    ListenedTimes: int | None = None
    Artists: List[RawArtistInfo] | None = None


async def insert_document_action(
        db: db_dependency,
        name: str,
        content_type: ContentTypes,
        single: bool,
        active: bool,
        image_file: UploadFile = File(None),
        color: str | None = None,
        description: str | None = None,
):
    color = pars_null(color)
    description = pars_null(description)

    document = models.Document()
    document.Name = name
    document.Color = color
    document.Description = description
    document.ContentType = content_type
    document.Single = single
    document.Active = active

    db.add(document)
    db.commit()

    root = make_path(document.DirectoryName, is_file=False)
    storage.put_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=root)

    for i in DocumentQualities.directories():
        p = make_path(root, i, is_file=False)
        storage.put_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=p)

    if image_file:
        file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        document.MainImage = file_name

        storage.upload_fileobj(image_file.file, Bucket=Buckets.DOCUMENT_BUCKET_NAME,
                               Key=make_path(root, file_name, is_file=True))

        db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'document created',
            'Document_Id': document.Id,
        },
    )


async def edit_document_action(
        db: db_dependency,
        document_id: int,
        name: str | None = None,
        image_file: UploadFile = File(None),
        color: str | None = None,
        description: str | None = None,
        content_type: ContentTypes | None = None,
        single: bool | None = None,
        active: bool | None = None,
        delete_image: bool | None = False,
):
    document = db.query(models.Document).where(models.Document.Id == document_id).first()
    document.Name = name if name is not None else document.Name
    document.Color = color
    document.Description = description
    document.ContentType = content_type if content_type is not None else document.ContentType
    document.Single = single if single is not None else document.Single
    document.Active = active if active is not None else document.Active

    main_path = make_path(document.DirectoryName, is_file=False)

    def delete_image_action(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.DOCUMENT_BUCKET_NAME)
        except Exception as ex_2:
            print(ex_2)

    if image_file and not delete_image:
        previous_image_file_name = document.MainImage
        new_image_file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        try:
            storage.upload_fileobj(
                image_file.file,
                Bucket=Buckets.DOCUMENT_BUCKET_NAME,
                Key=make_path(
                    main_path,
                    new_image_file_name,
                    is_file=True,
                )
            )
        except Exception as ex:
            print(ex)
            delete_image_action(new_image_file_name)
        else:
            try:
                delete_image_action(previous_image_file_name)
            except Exception as ex_1:
                print(ex_1)
                delete_image_action(new_image_file_name)
            else:
                document.MainImage = new_image_file_name
    elif not image_file and delete_image:
        try:
            delete_image_action(document.MainImage)
        except Exception as ex_1:
            print(ex_1)
        else:
            document.MainImage = None

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'document edited',
            'Document_Id': document.Id,
        },
    )


async def get_document_full_info(
        db: db_dependency,
        document: models.Document,
) -> DocumentFullInfo:
    artists = db.query(models.Artists).join(
        models.DocumentsOwners,
        models.Artists.Id == models.DocumentsOwners.ArtistId
    ).filter(
        models.DocumentsOwners.DocumentId == document.Id
    ).order_by(
        models.DocumentsOwners.OrderBy.asc().nullslast(),
        models.DocumentsOwners.Id.asc(),
    ).all()

    data = DocumentFullInfo()
    data.Id = document.Id
    data.Artists = [get_raw_artist_info(artist) for artist in artists]
    data.Name = document.Name
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    ) if document.MainImage else None
    data.Color = document.Color
    data.Description = document.Description
    data.Active = document.Active
    data.ContentType = document.ContentType
    data.EpisodesNumber = db.query(
        models.DocumentsEpisodes
    ).where(
        models.DocumentsEpisodes.DocumentId == document.Id
    ).count()
    data.ListenedTimes = await get_listened_times(db=db, document_id=document.Id)
    data.Saves = db.query(
        models.UserFollowing
    ).where(
        models.UserFollowing.DocumentId == document.Id
    ).count()
    data.Likes = db.query(
        models.UserLikes
    ).where(
        models.UserLikes.DocumentId == document.Id
    ).count()
    data.CreationDate = document.CreationDate
    data.Single = document.Single

    duration = db.query(
        func.sum(
            models.DocumentsEpisodes.Duration
        ),
    ).where(
        models.DocumentsEpisodes.DocumentId == document.Id
    ).scalar()
    data.Duration = get_formatted_duration(int(duration) if duration else 0)

    category = db.query(
        models.DocumentsCategories
    ).where(
        models.DocumentsCategories.DocumentId == document.Id
    ).order_by(
        models.DocumentsCategories.OrderBy.asc().nullslast(),
        models.DocumentsCategories.Id.asc(),
    ).all()

    data.Categories = [await get_child_to_parent(db, x, contains_self=True) for x in category]

    return data


async def get_document_short_info(
        db: db_dependency,
        document: models.Document,
) -> DocumentShortInfo:
    artists = db.query(models.Artists).join(
        models.DocumentsOwners,
        models.Artists.Id == models.DocumentsOwners.ArtistId
    ).filter(
        models.DocumentsOwners.DocumentId == document.Id
    ).order_by(
        models.DocumentsOwners.OrderBy.asc().nullslast(),
        models.DocumentsOwners.Id.asc(),
    ).all()

    data = DocumentShortInfo()
    data.Id = document.Id
    data.Name = document.Name
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(
            document.DirectoryName,
            document.MainImage,
            is_file=True
        )
    ) if document.MainImage else None

    data.Description = document.Description

    data.ContentType = document.ContentType

    data.Single = document.Single
    data.ListenedTimes = await get_listened_times(db=db, document_id=document.Id)
    data.Artists = [get_raw_artist_info(artist) for artist in artists]

    data.CreationDate = document.CreationDate

    return data
