import models
import uuid
import pathlib
from db_dependency import db_dependency
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from typing import List
from actions.response_model import ResponseMessage
from sqlalchemy import and_
from constants import ContentTypes
from actions.categories_actions import get_child_to_parent, category_data
from utills.parse_null import pars_null
from utills.path_manager import make_path
from storage import Buckets, storage, storage_delete_file

router = APIRouter(prefix="/category", tags=["Category"])


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

    response = {}

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
        response = {"Category_id": category.Id}
    elif name and category_type:
        category = models.Categories()
        category.Name = name
        category.Type = category_type
        category.ParentId = parent_id
        category.Active = active
        if image_file:
            category.Image = await upload_file(None, image_file)
        db.add(category)
        response = {"Category_id": category.Id}

    db.commit()

    return response


@router.put("/reorder_categories", status_code=status.HTTP_200_OK)
async def reorder_document_categories(
        db: db_dependency,
        categories_id: List[int],
        parent_id: str | None = None,
):
    parent_id = pars_null(parent_id)
    for i in categories_id:
        check = db.query(models.Categories).where(
            and_(
                models.Categories.Id == i,
                models.Categories.ParentId == parent_id,
            )
        ).first()
        if check:
            check.OrderBy = categories_id.index(i)
            db.commit()

    return ResponseMessage(error=False, message="category reordered")


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

    return ResponseMessage(error=False, message="category deleted")


@router.get("/fetch_categories", status_code=status.HTTP_200_OK)
async def fetch_categories(
        db: db_dependency,
        category_type: ContentTypes,
        parent_id: str | None = None,
        contains_child: bool = False,
):

    parent_id = pars_null(parent_id)

    result = []

    parents = db.query(models.Categories).where(
        models.Categories.Type == category_type
    ).where(
        models.Categories.ParentId == parent_id
    ).order_by(
        models.Categories.OrderBy.is_(None),
        models.Categories.OrderBy.asc(),
        models.Categories.Id.asc(),
    ).all()

    if contains_child:

        for i in parents:

            children = db.query(
                models.Categories
            ).where(
                models.Categories.Type == category_type
            ).where(
                models.Categories.ParentId == i.Id
            ).order_by(
                models.Categories.OrderBy.is_(None),
                models.Categories.OrderBy.asc(),
                models.Categories.Id.asc(),
            ).all()

            item = dict()
            item['parentId'] = i.ParentId
            item['parent'] = category_data(i)
            item['children'] = [
                category_data(child) for child in children if child is not None
            ]

            result.append(item)

    else:
        result = parents
    return result


@router.get("/fetch_single_category", status_code=status.HTTP_201_CREATED)
async def fetch_single_category(
        db: db_dependency,
        category_id: int,
        contains_child: bool = False,
):

    result = {
        'parentId': None,
        'parent': None,
        'children': [],
    }

    parent = db.query(
        models.Categories
    ).where(
        models.Categories.Id == category_id
    ).order_by(
        models.Categories.OrderBy.is_(None),
        models.Categories.OrderBy.asc()
    ).first()

    if not parent:
        raise HTTPException(404, "category not found!")

    if contains_child and parent:

        children = db.query(
            models.Categories
        ).where(
            models.Categories.ParentId == parent.Id
        ).order_by(
            models.Categories.OrderBy.is_(None),
            models.Categories.OrderBy.asc()
        ).all()

        result['parentId'] = parent.ParentId
        result['parent'] = category_data(parent)
        result['children'] = [
            category_data(child) for child in children if child is not None
        ]

    else:
        result = category_data(parent)
    return result


@router.get("/child_to_parent", status_code=status.HTTP_201_CREATED)
async def child_to_parent(
        db: db_dependency,
        category_id: int,
):
    return await get_child_to_parent(db, category_id, contains_self=True)
