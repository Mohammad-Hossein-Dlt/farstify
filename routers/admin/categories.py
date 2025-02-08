import models
import uuid
import pathlib
from db_dependency import db_dependency
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from typing import List
from actions.response_model import ResponseMessage
from constants import ContentTypes
from utills.parse_null import pars_null
from utills.path_manager import make_path
from storage import Buckets, storage, storage_delete_file

router = APIRouter(prefix="/admin/category", tags=["Admin-Category"])


@router.post("/insert_category", status_code=status.HTTP_201_CREATED)
async def insert_category(
        db: db_dependency,
        category_id: str | None = None,
        parent_id: str | None = None,
        name: str | None = None,
        category_type: ContentTypes | None = None,
        active: bool = True,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    category_id = pars_null(category_id)
    parent_id = pars_null(parent_id)
    name = pars_null(name)
    category_type = pars_null(category_type)

    response = ResponseMessage(
        Error=False,
        Content={
            'Message': 'category added',
            'Category_Id': 0,
        },
    )

    async def upload_file(previous_file_name: str | None, file: UploadFile) -> str:
        new_file_name = uuid.uuid4().hex[:8] + pathlib.Path(file.filename).suffix
        image_path = make_path(new_file_name, is_file=True)
        try:
            storage.upload_fileobj(file.file, Bucket=Buckets.CHUNKS_BUCKET_NAME, Key=image_path)
        except Exception as ex_1:
            print(ex_1)
        else:
            if previous_file_name:
                try:
                    previous_image = make_path(previous_file_name, is_file=True)
                    storage_delete_file(previous_image, Buckets.CHUNKS_BUCKET_NAME)
                except Exception as ex_2:
                    print(ex_2)
        return new_file_name

    if category_id:
        category = db.query(
            models.Categories
        ).where(
            models.Categories.Id == category_id
        ).first()
        if category is None:
            raise HTTPException(404, "episode not found!")
        category.Name = name if name else category.Name
        category.Active = active
        if image_file:
            category.Image = await upload_file(category.Image, image_file)
        elif delete_image:
            try:
                image = make_path(category.Image, is_file=True)
                storage_delete_file(image, Buckets.CHUNKS_BUCKET_NAME)
            except Exception as ex:
                print(ex)
            else:
                category.Image = None

        db.commit()
        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'category edited',
                'Category_Id': category.Id,
            },
        )
    elif name and category_type and not category_id:
        category = models.Categories()
        category.Name = name
        category.Type = category_type
        category.ParentId = parent_id
        category.Active = active
        if image_file:
            category.Image = await upload_file(None, image_file)
        db.add(category)
        db.commit()

        response = ResponseMessage(
            Error=False,
            Content={
                'Message': 'category added',
                'Category_Id': category.Id,
            },
        )

    return response


@router.put("/reorder_categories", status_code=status.HTTP_200_OK)
async def reorder_document_categories(
        db: db_dependency,
        categories_id: List[int],
        category_type: ContentTypes,
        parent_id: int | str | None = None,
):
    parent_id = pars_null(parent_id)

    categories = db.query(
        models.Categories
    ).where(
        models.Categories.Type == category_type,
        models.Categories.ParentId == parent_id,
    ).all()

    for index, category_id in enumerate(categories_id):
        for category in categories:
            if category.Id == category_id:
                category.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'category reordered',
        },
    )


@router.delete("/delete_category", status_code=status.HTTP_200_OK)
async def fetch_category(
        db: db_dependency,
        category_id: int,
):
    category = db.query(
        models.Categories
    ).where(
        models.Categories.Id == category_id
    ).first()

    if not category:
        raise HTTPException(404, "category not found!")

    if category.Image:
        try:
            delete_image = make_path(category.Image, is_file=True)
            storage_delete_file(delete_image, Buckets.CHUNKS_BUCKET_NAME)
        except Exception as ex:
            raise HTTPException(500, "unable to delete category completely!")
    db.delete(category)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'category deleted',
        },
    )
