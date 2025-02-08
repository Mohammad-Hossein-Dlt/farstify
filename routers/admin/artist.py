import models
import uuid
import pathlib
from actions.link_actions import get_link_data
from storage import storage, Buckets, storage_delete_file, storage_delete_folder
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from actions.response_model import ResponseMessage
from typing import List
from sqlalchemy import and_
from utills.parse_null import pars_null
from utills.path_manager import make_path
from constants import ContentTypes, Socials
from actions.artist_images_actions import get_artist_image_info, ArtistImageInfo

router = APIRouter(prefix="/admin/artist", tags=["Admin-Artist"])


@router.post("/insert_artist", status_code=status.HTTP_201_CREATED)
async def insert_artist(
        db: db_dependency,
        artist_id: int | None = None,
        name: str | None = None,
        content_type: ContentTypes | None = None,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    artist_id = pars_null(artist_id)
    name = pars_null(name)
    content_type = pars_null(content_type)

    response = ResponseMessage(
        Error=False,
        Content={
            'Message': 'artist profile edited!',
            'Artist_Id': 0,
        },
    )

    async def upload_image(previous_file_name: str | None, directoryName: str) -> str:
        new_file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(directoryName, new_file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            if previous_file_name:
                try:
                    image_path = make_path(directoryName, previous_file_name, is_file=True)
                    storage_delete_file(image_path, Buckets.USER_BUCKET_NAME)
                except Exception as ex:
                    print(ex)
        return new_file_name

    if not artist_id:

        if name is None or content_type is None:
            raise HTTPException(422, 'name and content_type must be given')

        check = db.query(
            models.Artists
        ).where(
            models.Artists.Name == name
        ).first()

        if check:
            raise HTTPException(403, "artist already exists!")

        artist = models.Artists()
        artist.Name = name.strip()
        artist.ContentType = content_type
        db.add(artist)

        db.commit()

        path = make_path(artist.DirectoryName, is_file=False)
        storage.put_object(Bucket=Buckets.USER_BUCKET_NAME, Key=path)
        if image_file:
            artist.ProfileImage = await upload_image(None, artist.DirectoryName)
            db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'artist profile edited!',
                'Artist_Id': artist.Id,
            },
        )

    elif artist_id:

        artist = db.query(
            models.Artists
        ).where(
            models.Artists.Id == artist_id
        ).first()

        if not artist:
            raise HTTPException(404, "artist not found!")

        artist.Name = name.strip() if name else artist.Name
        artist.ContentType = content_type if content_type else artist.ContentType

        if image_file:
            artist.ProfileImage = await upload_image(artist.ProfileImage, artist.DirectoryName)
        elif delete_image:
            try:
                path = make_path(artist.DirectoryName, artist.ProfileImage, is_file=True)
                storage_delete_file(path, Buckets.USER_BUCKET_NAME)
            except Exception as ex:
                print(ex)
            else:
                artist.ProfileImage = None

        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'artist profile edited!',
                'Artist_Id': artist.Id,
            },
        )

    return response


@router.get("/fetch_images", status_code=status.HTTP_201_CREATED)
async def fetch_images(
        db: db_dependency,
        artist_id: int,
):
    result: List[ArtistImageInfo] = list()

    artist = db.query(
        models.Artists
    ).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, "artist not found!")

    images = db.query(
        models.ArtistImages
    ).where(
        models.ArtistImages.ArtistId == artist.Id,
    ).order_by(
        models.ArtistImages.OrderBy.asc().nullslast(),
        models.ArtistImages.Id.asc(),
    ).all()

    for img in images:
        result.append(get_artist_image_info(artist=artist, image=img))

    return result


@router.post("/edit_image", status_code=status.HTTP_201_CREATED)
async def artist_image(
        db: db_dependency,
        artist_id: int,
        image_id: int | str | None = None,
        image_file: UploadFile = File(None),
        delete_image: bool | str | None = None,
):
    image_id = pars_null(image_id)
    delete_image = pars_null(delete_image)

    response = ResponseMessage(
        Error=False,
        Content={
            'Message': 'artist image edited!',
            'Image_Id': 0,
        },
    )

    artist = db.query(
        models.Artists
    ).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, "artist not found!")

    async def upload_image(previous_file_name: str | None, directoryName: str) -> str:
        new_file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(directoryName, new_file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            if previous_file_name:
                try:
                    image_path = make_path(directoryName, previous_file_name, is_file=True)
                    storage_delete_file(image_path, Buckets.USER_BUCKET_NAME)
                except Exception as ex:
                    print(ex)
        return new_file_name

    if image_id:

        image = db.query(
            models.ArtistImages
        ).where(
            and_(
                models.ArtistImages.Id == image_id,
                models.ArtistImages.ArtistId == artist_id,
            )
        ).first()

        if not image:
            raise HTTPException(404, "artist image not found!")

        if image_file:
            image.Image = await upload_image(image.Image, artist.DirectoryName)
            response = ResponseMessage(
                Error=False,
                Content={
                    'Message': 'artist image edited!',
                    'Image_Id': image.Id,
                },
            )
        elif delete_image:
            try:
                path = make_path(artist.DirectoryName, image.Image, is_file=True)
                storage_delete_file(path, Buckets.USER_BUCKET_NAME)
            except Exception as ex:
                print(ex)
            else:
                db.delete(image)
                response = ResponseMessage(
                    Error=False,
                    Content={
                        'Message': 'image deleted!',
                        'Image_Id': image.Id,
                    },
                )

        db.commit()

    else:
        image = models.ArtistImages()
        image.ArtistId = artist_id

        if image_file:
            image.Image = await upload_image(None, artist.DirectoryName)
        db.add(image)
        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'image added!',
                'Image_Id': image.Id,
            },
        )

    return response


@router.put("/reorder_images", status_code=status.HTTP_200_OK)
async def reorder_images(
        db: db_dependency,
        artist_id: int,
        images_id: List[int],
):
    get_images = db.query(
        models.ArtistImages
    ).where(
        models.ArtistImages.ArtistId == artist_id,
    ).all()

    for index, image_id in enumerate(images_id):
        for image in get_images:
            if image.Id == image_id:
                image.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'images reordered!',
        },
    )


@router.get("/fetch_links", status_code=status.HTTP_200_OK)
async def fetch_links(
        db: db_dependency,
        artist_id: int,
):
    links = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.ArtistId == artist_id,
    ).order_by(
        models.ArtistLinks.OrderBy.asc().nullslast(),
        models.ArtistLinks.Id.asc(),
    ).all()

    return [get_link_data(link) for link in links]


@router.post("/insert_link", status_code=status.HTTP_200_OK)
async def insert_link(
        db: db_dependency,
        artist_id: int | None = None,
        link_id: int | None = None,
        title: str | None = None,
        url: str | None = None,
        link_type: Socials | None = None,
):
    artist_id = pars_null(artist_id)
    link_id = pars_null(link_id)
    title = pars_null(title)
    url = pars_null(url)
    link_type = pars_null(link_type)

    # params = [artist_id, link_id]
    # given_params = sum(p is not None for p in params)
    #
    # if given_params > 1:
    #     raise HTTPException(403, "only one entity (artist_id or link_id) must be given")
    # elif given_params == 0:
    #     raise HTTPException(403, "one entity (artist_id or link_id) must be given")

    response = ResponseMessage(
        Error=False,
        Content={
            'Message': 'link edited!',
            'Artist_Link_Id': 0,
        },
    )

    if link_id:

        artist_link = db.query(
            models.ArtistLinks
        ).where(
            models.ArtistLinks.Id == link_id,
        ).first()

        if not artist_link:
            raise HTTPException(404, "artist link not found!")

        artist_link.Title = title if title is not None else artist_link.Title
        artist_link.Url = url if url is not None else artist_link.Url
        artist_link.Type = link_type if link_type is not None else artist_link.Type

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'link edited!',
                'Artist_Link_Id': artist_link.Id,
            },
        )
    elif artist_id:

        if title is None or url is None or link_type is None:
            raise HTTPException(422, "title, link or link_type submitted incorrectly!")

        artist_link = models.ArtistLinks()
        artist_link.ArtistId = artist_id,
        artist_link.Title = title
        artist_link.Url = url
        artist_link.Type = link_type

        db.add(artist_link)

        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'link added!',
                'Artist_Link_Id': artist_link.Id,
            },
        )

    db.commit()
    return response


@router.get("/fetch_single_link", status_code=status.HTTP_200_OK)
async def fetch_single_link(
        db: db_dependency,
        link_id: int,
):
    link = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.Id == link_id,
    ).first()

    if not link:
        raise HTTPException(404, "link not found!")

    return get_link_data(link)


@router.put("/reorder_links", status_code=status.HTTP_200_OK)
async def reorder_link(
        db: db_dependency,
        artist_id: int,
        links_id: List[int],
):
    get_links = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.ArtistId == artist_id,
    ).all()

    for index, link_id in enumerate(links_id):
        for link in get_links:
            if link.Id == link_id:
                link.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'artist links reordered!',
        },
    )


@router.delete("/delete_link", status_code=status.HTTP_200_OK)
async def delete_link(
        db: db_dependency,
        link_id: int,
):
    link = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.Id == link_id,
    ).first()

    if not link:
        raise HTTPException(404, "artist link not found!")

    db.delete(link)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'link deleted!',
        },
    )


@router.delete("/delete_artist", status_code=status.HTTP_200_OK)
async def reorder_link(
        db: db_dependency,
        artist_id: int,
):
    artist = db.query(
        models.Artists
    ).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, "artist not found!")

    try:
        storage_delete_folder(artist.DirectoryName, Buckets.USER_BUCKET_NAME)
    except Exception as ex:
        raise HTTPException(500, "unable to delete artist completely!")
    else:
        db.delete(artist)
        db.commit()
        return ResponseMessage(
            Error=False,
            Content={
                'Message': 'artist deleted!',
            },
        )
