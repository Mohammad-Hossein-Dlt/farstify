import models
from actions.categories_actions import get_child_to_parent
from actions.document_actions import insert_document_action, edit_document_action
from db_dependency import db_dependency
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from constants import ContentTypes
from storage import Buckets, storage_delete_folder
from typing import List

router = APIRouter(prefix="/admin/document", tags=["Admin-Document"])


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
    if not document_id:
        if name is None or content_type is None or single is None or active is None:
            raise HTTPException(422, "name, content_type, single or active submitted incorrectly!")

        return await insert_document_action(
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
        return await edit_document_action(
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


@router.post("/insert_document_category", status_code=status.HTTP_200_OK)
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

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'document new category inserted',
            'Document_category_Id': category.Id,
        },
    )


@router.delete("/delete_document_category", status_code=status.HTTP_200_OK)
async def delete_document_category(
        db: db_dependency,
        document_category_id: int,

):
    category = db.query(models.DocumentsCategories).where(
        models.DocumentsCategories.CategoryId == document_category_id,
    ).first()

    if not category:
        raise HTTPException(404, "document category not found!")

    db.delete(category)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'document category deleted',
        },
    )


@router.get("/get_document_categories", status_code=status.HTTP_200_OK)
async def get_document_categories(
        db: db_dependency,
        document_id: int,
):
    result = []

    document_categories = db.query(
        models.DocumentsCategories,
    ).where(
        models.DocumentsCategories.DocumentId == document_id,
    ).order_by(
        models.DocumentsCategories.OrderBy.asc().nullslast(),
        models.DocumentsCategories.Id.asc(),
    ).all()

    return [
        await get_child_to_parent(db=db, document_category=x, contains_self=True)
        for x in document_categories
    ]


@router.put("/reorder_document_categories", status_code=status.HTTP_200_OK)
async def reorder_document_categories(
        db: db_dependency,
        document_id: int,
        categories_id: List[int],
):
    document_categories = db.query(
        models.DocumentsCategories
    ).where(
        models.DocumentsCategories.DocumentId == document_id,
    ).all()

    for index, document_category_id in enumerate(categories_id):
        for document_category in document_categories:
            if document_category.Id == document_category_id:
                document_category.OrderBy = index

    db.commit()

    # return ResponseMessage(error=False, message="document categories reordered")
    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'document categories reordered',
        },
    )


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

        return ResponseMessage(
            Error=False,
            Content={
                'Message': 'document deleted',
            },
        )
