import models
import pathlib
import uuid

from actions.categories_actions import category_data
from db_dependency import db_dependency
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from constants import ContentTypes, DocumentQualities
from utills.path_manager import make_path
from utills.exceptions import owned_exception
from utills.check_ownership import is_document_owned_by_artist
from storage import storage, Buckets, storage_delete_folder, storage_delete_file
from typing import List

router = APIRouter()


@router.post("/insert-document", status_code=status.HTTP_201_CREATED, tags=["Document"])
async def insert_document(
        db: db_dependency,
        artist_id: int,
        image_file: UploadFile,
        name: str,
        description: str,
        content_type: ContentTypes,
        single: bool = True,
        active: bool = True,
):
    the_document = models.Document()
    the_document.Owner = artist_id
    the_document.Name = name
    the_document.Description = description
    the_document.ContentType = content_type
    the_document.Active = active
    the_document.Single = single
    db.add(the_document)

    file_name = uuid.uuid4().hex[:8] + pathlib.Path(image_file.filename).suffix
    the_document.MainImage = file_name
    db.commit()

    path = make_path(the_document.DirectoryName, is_file=False)

    storage.put_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=path)

    for i in DocumentQualities.directories():
        p = make_path(the_document.DirectoryName, i, is_file=False)
        storage.put_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=p)

    preview_path = make_path(the_document.DirectoryName, DocumentQualities.preview, is_file=False)
    storage.put_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=preview_path)

    storage.upload_fileobj(image_file.file, Bucket=Buckets.DOCUMENT_BUCKET_NAME,
                           Key=make_path(path, file_name, is_file=True))

    return ResponseMessage(error=False, message="Document created!")


@router.put("/update-document", status_code=status.HTTP_200_OK, tags=["Document"])
async def update_document(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        main_image: UploadFile = File(None),
        name: str | None = None,
        description: str | None = None,
        content_type: ContentTypes | None = None,
        # IsPaid: BoolEnum | None = None,
        active: bool | None = None,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    the_document = db.query(models.Document).where(models.Document.Id == document_id).first()
    the_document.Name = name if name is not None else the_document.Name
    the_document.Description = description if description is not None else the_document.Description
    # theDocument.IsPaid = IsPaid if IsPaid is not None else theDocument.IsPaid
    the_document.Active = active if active is not None else the_document.Active
    the_document.ContentType = content_type if content_type is not None else the_document.ContentType

    main_path = make_path(the_document.DirectoryName, is_file=False)

    def delete_image(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.DOCUMENT_BUCKET_NAME)
        except Exception as ex_2:
            print(ex_2)

    if main_image:

        old_main_image = the_document.MainImage

        file_name = uuid.uuid4().hex + pathlib.Path(main_image.filename).suffix

        try:
            storage.upload_fileobj(main_image.file, Bucket=Buckets.DOCUMENT_BUCKET_NAME,
                                   Key=make_path(main_path, file_name, is_file=True))
        except Exception as ex:
            print(ex)
            delete_image(file_name)
        else:
            try:
                delete_image(old_main_image)
            except Exception as ex_1:
                print(ex_1)
                delete_image(file_name)
            else:
                the_document.MainImage = file_name

    db.commit()
    return ResponseMessage(error=False, message="Document updated!")


# @router.put("/insert-document-labels", status_code=status.HTTP_200_OK, tags=["Document"])
# async def insert_document_labels(
#         db: db_dependency,
#         artist_id: int,
#         document_id: int,
#         labels: List[str],
# ):
#     if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
#         raise owned_exception
#
#     if len(labels) != 0:
#         labels = [x.strip() for x in labels]
#         get_labels = db.query(models.DocumentsLabels).where(
#             models.DocumentsLabels.DocumentId == document_id).all()
#         previous_labels: List[str] = [x.Title for x in get_labels]
#
#         to_delete = set(previous_labels) - set(labels)
#         to_add = set(labels) - set(previous_labels)
#
#         delete = db.query(models.DocumentsLabels).where(
#             and_(
#                 models.DocumentsLabels.DocumentId == document_id,
#                 models.DocumentsLabels.Title.in_(to_delete)
#             )
#         ).all()
#         for i in delete:
#             db.delete(i)
#         for i in to_add:
#             v = {"DocumentId": document_id, "Title": i.strip()}
#             ep = models.DocumentsLabels(**v)
#             db.add(ep)
#
#         db.commit()
#
#
# @router.put("/get-document-labels", status_code=status.HTTP_200_OK, tags=["Document"])
# async def get_document_labels(
#         db: db_dependency,
#         document_id: int,
# ):
#     labels = db.query(models.DocumentsLabels).where(
#         models.DocumentsLabels.DocumentId == document_id,
#     ).all()
#     return [{"id": x.Id, "title": x.Title} for x in labels]


@router.put("/insert-document-categories", status_code=status.HTTP_200_OK, tags=["Document"])
async def insert_document_categories(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        category_id: int,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception

    check = db.query(models.DocumentsCategories).where(
        and_(
            models.DocumentsCategories.DocumentId == document_id,
            models.DocumentsCategories.CategoryId == category_id,
        )
    ).first()
    if not check:
        category = {"DocumentId": document_id, "CategoryId": category_id}
        ep = models.DocumentsCategories(**category)
        db.add(ep)
        db.commit()
        return ResponseMessage(error=False, message="Document's new category inserted!")
    else:
        raise HTTPException(404, "the category already added!")


@router.delete("/delete-document-category", status_code=status.HTTP_200_OK, tags=["Document"])
async def delete_document_category(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        category_id: int,

):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    category = db.query(models.DocumentsCategories).where(
        and_(
            models.DocumentsCategories.DocumentId == document_id,
            models.DocumentsCategories.CategoryId == category_id,
        )
    ).first()
    db.delete(category)
    db.commit()

    return ResponseMessage(error=False, message="Document's category deleted!")


@router.put("/get-document-categories", status_code=status.HTTP_200_OK, tags=["Document"])
async def get_document_categories(
        db: db_dependency,
        document_id: int,
):
    categories = db.query(models.Categories).join(
        models.DocumentsCategories
    ).where(
        models.DocumentsCategories.DocumentId == document_id,
    ).order_by(
        models.DocumentsCategories.OrderBy.is_(None),
        models.DocumentsCategories.OrderBy.asc()
    ).all()
    return [category_data(x) for x in categories]


@router.put("/reorder-document-categories", status_code=status.HTTP_200_OK, tags=["Document"])
async def reorder_document_categories(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        categories_id: List[int],
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    for i in categories_id:
        check = db.query(models.DocumentsCategories).where(
            and_(
                models.DocumentsCategories.CategoryId == i,
                models.DocumentsCategories.DocumentId == document_id,
            )
        ).first()
        if check:
            check.OrderBy = categories_id.index(i)
            db.commit()

    return ResponseMessage(error=False, message="Document categories reordered!")


@router.put("/insert-document-link", status_code=status.HTTP_200_OK, tags=["Document"])
async def insert_document_link(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        link: str,
        title: str | None = None,
        link_id: int | None = None,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    if link_id:
        document_link = db.query(models.DocumentsLinks).where(
            and_(
                models.DocumentsLinks.Id == link_id,
                models.DocumentsLinks.DocumentId == document_id,
            )
        ).first()
        if document_link:
            document_link.Title = title
            document_link.Link = link
    else:
        document_link = models.DocumentsLinks()
        document_link.Title = title
        document_link.DocumentId = document_id
        document_link.Link = link

        db.add(document_link)

    db.commit()

    return ResponseMessage(error=False, message="Document's new link inserted!")


@router.delete("/delete-document-link", status_code=status.HTTP_200_OK, tags=["Document"])
async def delete_document_link(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        link_id: int,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    link = db.query(models.DocumentsLinks).where(
        and_(
            models.DocumentsLinks.DocumentId == document_id,
            models.DocumentsLinks.Id == link_id,
        )
    ).first()
    db.delete(link)
    db.commit()

    return ResponseMessage(error=False, message="Document link deleted!")


@router.put("/get-document-linkS", status_code=status.HTTP_200_OK, tags=["Document"])
async def get_document_link(
        db: db_dependency,
        document_id: int,
):
    labels = db.query(models.DocumentsLinks).where(
        models.DocumentsLinks.DocumentId == document_id,
    ).order_by(
        models.DocumentsLinks.OrderBy.is_(None),
        models.DocumentsLinks.OrderBy.asc()
    ).all()
    return [{"id": x.Id, "title": x.Title, "link": x.Link} for x in labels]


@router.put("/reorder-document-linkS", status_code=status.HTTP_200_OK, tags=["Document"])
async def reorder_document_link(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        links_id: List[int],
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception

    get_links = db.query(models.DocumentsLinks).where(
        and_(
            models.DocumentsLinks.DocumentId == document_id,
        )
    ).all()

    for index, link_id in enumerate(links_id):
        for link in get_links:
            if link.Id == link_id:
                link.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message="Document links reordered!")


@router.delete("/delete-document", status_code=status.HTTP_200_OK, tags=["Document"])
async def delete_document(
        db: db_dependency,
        artist_id: int,
        document_id: int,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception
    theDocument = db.query(models.Document).where(models.Document.Id == document_id).first()
    try:
        storage_delete_folder(theDocument.DirectoryName, Buckets.DOCUMENT_BUCKET_NAME)
    except Exception as ex:
        print(ex)
    else:
        db.delete(theDocument)
        db.commit()

        return ResponseMessage(error=False, message="Document deleted!")
