import models
import uuid
import pathlib
from passlib.context import CryptContext

from actions.artist_short_info_actions import get_artist_short_info
from storage import storage, Buckets, storage_delete_file
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from actions.response_model import ResponseMessage
from typing import List
from sqlalchemy import and_

from utills.parse_null import pars_null
from utills.path_manager import make_path
from constants import ContentTypes
from actions.artist_images_actions import artist_image_view_model, ImageViewModel

router = APIRouter(prefix="/artist", tags=["Artist"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AddArtist(BaseModel):
    Name: str
    ContentType: ContentTypes


@router.get("/fetch_all_artists", status_code=status.HTTP_201_CREATED)
async def add_artist(
        db: db_dependency,
        limit: int,
        page: int,
):
    artists = db.query(models.Artists).limit(limit).offset(limit * page).all()

    return [get_artist_short_info(i) for i in artists]


@router.post("/add_artist", status_code=status.HTTP_201_CREATED)
async def add_artist(
        db: db_dependency,
        name: str,
        content_type: ContentTypes
):
    check = db.query(models.Artists).where(models.Artists.Name == name).first()

    if check:
        raise HTTPException(201, "artist already added!")

    artist = models.Artists()
    artist.Name = name.strip()
    artist.ContentType = content_type
    db.add(artist)

    db.commit()

    path = make_path(artist.DirectoryName, is_file=False)
    storage.put_object(Bucket=Buckets.USER_BUCKET_NAME, Key=path)

    return ResponseMessage(error=False, message="artist has been signed up!")


@router.post("/change-profile-image", status_code=status.HTTP_201_CREATED)
async def change_profile_image(
        db: db_dependency,
        artist_id: int,
        image_file: UploadFile = File(None),
        delete_image: bool = False,

):
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    main_path = make_path(artist.DirectoryName, is_file=False)

    def delete_image_action(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.USER_BUCKET_NAME)
        except Exception as ex_2:
            print(ex_2)

    if image_file and not delete_image:
        file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(main_path, file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
            delete_image_action(file_name)
        else:
            try:
                delete_image_action(artist.ProfileImage)
            except Exception as ex_1:
                delete_image_action(file_name)
                print(ex_1)
            else:
                artist.ProfileImage = file_name
                db.commit()
    elif not image_file and delete_image:
        try:
            delete_image_action(artist.ProfileImage)
        except Exception as ex_1:
            print(ex_1)
        else:
            artist.ProfileImage = None
            db.commit()
    return ResponseMessage(error=False, message="artist profile image has been changed!")


@router.post("/fetch-profile-images", status_code=status.HTTP_201_CREATED)
async def change_profile_image(
        db: db_dependency,
        artist_id: int,
):
    result: List[ImageViewModel] = list()

    artist = db.query(models.Artists).where(
        models.Artists.Id == artist_id
    ).first()

    images = db.query(models.ArtistImages).where(
        models.ArtistImages.ArtistId == artist_id
    ).order_by(
        models.ArtistImages.OrderBy.is_(None),
        models.ArtistImages.OrderBy.asc()
    ).all()

    for img in images:
        result.append(artist_image_view_model(artist=artist, image=img))

    return result


@router.post("/artist_image", status_code=status.HTTP_201_CREATED)
async def artist_image(
        db: db_dependency,
        artist_id: int,
        image_file: UploadFile = File(None),
        image_id: int | None = None,
        delete_image: bool = False,
):
    image_id = pars_null(image_id)

    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()
    main_path = make_path(artist.DirectoryName, is_file=False)

    def delete_image_action(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.USER_BUCKET_NAME)
        except Exception as ex_2:
            print(ex_2)

    if image_file and not delete_image:
        file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(main_path, file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            if image_id:

                artist_img = db.query(models.ArtistImages).where(
                    and_(
                        models.ArtistImages.Id == image_id,
                        models.ArtistImages.ArtistId == artist_id,
                    )
                ).first()

                if artist_img:
                    try:
                        delete_image_action(artist_img.Image)
                    except Exception as ex_1:
                        print(ex_1)
                        delete_image_action(file_name)
                    else:
                        artist_img.Image = file_name

            else:

                artist_img = models.ArtistImages()
                artist_img.ArtistId = artist.Id
                artist_img.Image = file_name
                db.add(artist_img)

            db.commit()

    elif not image_file and delete_image and image_id:
        artist_img = db.query(models.ArtistImages).where(
            and_(
                models.ArtistImages.Id == image_id,
                models.ArtistImages.ArtistId == artist_id,
            )
        ).first()
        if artist_img:
            try:
                delete_image_action(artist_img.Image)
            except Exception as ex_1:
                print(ex_1)
            else:
                db.delete(artist_img)
                db.commit()
    return ResponseMessage(error=False, message="artist profile image has been changed!")


@router.put("/reorder_images", status_code=status.HTTP_200_OK)
async def reorder_images(
        db: db_dependency,
        artist_id: int,
        images_id: List[int],
):
    get_images = db.query(models.ArtistImages).where(
        and_(
            models.ArtistImages.ArtistId == artist_id,
        )
    ).all()

    for index, image_id in enumerate(images_id):
        for image in get_images:
            if image.Id == image_id:
                image.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message="Links has been reordered!")


@router.put("/edit_profile", status_code=status.HTTP_201_CREATED)
async def edit_profile(
        db: db_dependency,
        artist_id: int,
        name: str | None = None,
):
    name = pars_null(name)

    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()
    artist.Name = name.strip() if name else artist.Name

    db.commit()
    return ResponseMessage(error=False, message="User profile has been changed!")


@router.put("/insert_link", status_code=status.HTTP_200_OK)
async def insert_link(
        db: db_dependency,
        artist_id: int,
        link: str,
        title: str | None = None,
        link_id: int | None = None,
):
    title = pars_null(title)
    link_id = pars_null(link_id)

    if link_id:
        artist_link = db.query(models.ArtistLinks).where(
            and_(
                models.ArtistLinks.Id == link_id,
                models.ArtistLinks.ArtistId == artist_id,
            )
        ).first()

        if not artist_link:
            raise HTTPException(404, "an error occurred!")

        artist_link.Title = title
        artist_link.Link = link
        db.commit()

        return ResponseMessage(error=False, message="Link has been updated!")
    else:
        artist_link = models.ArtistLinks()
        artist_link.Title = title
        artist_link.ArtistId = artist_id,
        artist_link.Link = link

        db.add(artist_link)

        db.commit()

        return ResponseMessage(error=False, message="Link has been inserted!")


@router.delete("/delete_link", status_code=status.HTTP_200_OK)
async def delete_link(
        db: db_dependency,
        artist_id: int,
        link_id: int,
):
    link = db.query(models.ArtistLinks).where(
        and_(
            models.ArtistLinks.ArtistId == artist_id,
            models.ArtistLinks.Id == link_id,
        )
    ).first()
    if link:
        db.delete(link)
        db.commit()
    return ResponseMessage(error=False, message="Link has been deleted!")


@router.put("/get_links", status_code=status.HTTP_200_OK)
async def get_link(
        db: db_dependency,
        artist_id: int,
):
    links = db.query(models.ArtistLinks).where(
        models.ArtistLinks.ArtistId == artist_id,
    ).order_by(
        models.ArtistLinks.OrderBy.is_(None),
        models.ArtistLinks.OrderBy.asc()
    ).all()
    return [{"id": x.Id, "title": x.Title, "link": x.Link} for x in links]


@router.put("/reorder_link", status_code=status.HTTP_200_OK)
async def reorder_link(
        db: db_dependency,
        artist_id: int,
        links_id: List[int],
):
    get_links = db.query(models.ArtistLinks).where(
        and_(
            models.ArtistLinks.ArtistId == artist_id,
        )
    ).all()

    for index, link_id in enumerate(links_id):
        for link in get_links:
            if link.Id == link_id:
                link.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message="Links has been reordered!")
