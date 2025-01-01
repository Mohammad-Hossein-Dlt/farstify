import models
from actions.categories_actions import category_data
from actions.document_actions import insert_document_action, edit_document_action
from db_dependency import db_dependency
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from constants import ContentTypes
from storage import Buckets, storage_delete_folder
from typing import List

router = APIRouter(prefix="/document", tags=["Document"])


@router.post("/insert_document", status_code=status.HTTP_201_CREATED)
async def insert_document(
        db: db_dependency,
        document_id: int | None = None,
        name: str | None = None,
        image_file: UploadFile = File(None),
        color: str | None = None,
        description: str | None = None,
        content_type: ContentTypes | None = None,
        single: bool | None = None,
        active: bool | None = None,
        delete_image: bool = False,
):
    # params = [artist_id, document_id]
    # given_params = sum(p is not None for p in params)
    #
    # if given_params > 1:
    #     raise HTTPException(403, "only one entity (artist_id or document_id) must be given")
    # elif given_params == 0:
    #     raise HTTPException(403, "one entity (artist_id or document_id) must be given")

    if not document_id:
        if name is None or content_type is None or single is None or active is None:
            raise HTTPException(422, "name, content_type, single or active submitted incorrectly")

        await insert_document_action(
            db=db,
            name=name,
            image_file=image_file,
            color=color,
            description=description,
            content_type=content_type,
            single=single,
            active=active,
        )

    elif document_id:
        await edit_document_action(
            db=db,
            document_id=document_id,
            name=name,
            image_file=image_file,
            color=color,
            description=description,
            content_type=content_type,
            single=single,
            active=active,
            delete_image=delete_image,
        )


@router.put("/insert_document_categories", status_code=status.HTTP_200_OK)
async def insert_document_categories(
        db: db_dependency,
        document_id: int,
        category_id: int,
):
    category = db.query(models.DocumentsCategories).where(
        and_(
            models.DocumentsCategories.DocumentId == document_id,
            models.DocumentsCategories.CategoryId == category_id,
        )
    ).first()

    if category:
        raise HTTPException(403, "document category already exists!")

    category = models.DocumentsCategories()
    category.DocumentId = document_id
    category.CategoryId = category_id

    db.add(category)
    db.commit()
    return ResponseMessage(error=False, message="document new category inserted")


@router.delete("/delete_document_category", status_code=status.HTTP_200_OK)
async def delete_document_category(
        db: db_dependency,
        document_id: int,
        category_id: int,

):
    category = db.query(models.DocumentsCategories).where(
        and_(
            models.DocumentsCategories.DocumentId == document_id,
            models.DocumentsCategories.CategoryId == category_id,
        )
    ).first()

    if not category:
        raise HTTPException(404, "document category not found!")

    db.delete(category)
    db.commit()

    return ResponseMessage(error=False, message="document category deleted")


@router.put("/get_document_categories", status_code=status.HTTP_200_OK)
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


@router.put("/reorder_document_categories", status_code=status.HTTP_200_OK)
async def reorder_document_categories(
        db: db_dependency,
        document_id: int,
        categories_id: List[int],
):
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

    return ResponseMessage(error=False, message="document categories reordered")


@router.put("/insert_document_link", status_code=status.HTTP_200_OK)
async def insert_document_link(
        db: db_dependency,
        document_id: int,
        link: str,
        title: str | None = None,
        link_id: int | None = None,
):
    if link_id:

        document_link = db.query(models.DocumentsLinks).where(
            and_(
                models.DocumentsLinks.Id == link_id,
                models.DocumentsLinks.DocumentId == document_id,
            )
        ).first()

        if not document_link:
            raise HTTPException(404, "document link not found!")

        document_link.Title = title
        document_link.Link = link

        response = ResponseMessage(error=False, message="document link updated")

    else:
        document_link = models.DocumentsLinks()
        document_link.Title = title
        document_link.DocumentId = document_id
        document_link.Link = link

        db.add(document_link)

        response = ResponseMessage(error=False, message="document new link added")

    db.commit()
    return response


@router.delete("/delete_document_link", status_code=status.HTTP_200_OK)
async def delete_document_link(
        db: db_dependency,
        document_id: int,
        link_id: int,
):
    link = db.query(models.DocumentsLinks).where(
        and_(
            models.DocumentsLinks.DocumentId == document_id,
            models.DocumentsLinks.Id == link_id,
        )
    ).first()

    if not link:
        raise HTTPException(404, "document link not found!")

    db.delete(link)
    db.commit()

    return ResponseMessage(error=False, message="document link deleted")


@router.put("/get_document_linkS", status_code=status.HTTP_200_OK)
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

    return [
        {
            "id": x.Id,
            "title": x.Title,
            "link": x.Link
        } for x in labels
    ]


@router.put("/reorder_document_linkS", status_code=status.HTTP_200_OK)
async def reorder_document_link(
        db: db_dependency,
        document_id: int,
        links_id: List[int],
):
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
    return ResponseMessage(error=False, message="document links reordered")


@router.delete("/delete_document", status_code=status.HTTP_200_OK)
async def delete_document(
        db: db_dependency,
        document_id: int,
):
    the_document = db.query(models.Document).where(models.Document.Id == document_id).first()

    if not the_document:
        raise HTTPException(404, "document not found!")

    try:
        storage_delete_folder(the_document.DirectoryName, Buckets.DOCUMENT_BUCKET_NAME)
    except Exception as ex:
        print(ex)
        raise HTTPException(500, "unable to delete document completely!!")
    else:
        db.delete(the_document)
        db.commit()
        return ResponseMessage(error=False, message="document deleted")
