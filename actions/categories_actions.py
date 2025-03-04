from typing import List
from fastapi import HTTPException
import models
from pydantic import BaseModel
from constants import ContentTypes
from db_dependency import db_dependency
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path


class CategoryInfo(BaseModel):
    Id: int | None = None
    ParentId: int | None = None
    Name: str | None = None
    Active: bool | None = None
    ImageUrl: str | None = None
    Type: ContentTypes | None = None
    OrderBy: int | None = None


class ChildToParent(BaseModel):
    Id: int | None = None
    Type: str | None = None
    Categories: List[CategoryInfo] | None = None


def category_data(
        category: models.Categories
) -> CategoryInfo:
    data = CategoryInfo()
    data.Id = category.Id
    data.ParentId = category.ParentId
    data.Name = category.Name
    data.Active = category.Active
    data.ImageUrl = encode_link(
        bucket_name=Buckets.CHUNKS_BUCKET_NAME,
        path=make_path(category.Image, is_file=True)
    ) if category.Image else None
    data.Type = category.Type
    data.OrderBy = category.OrderBy
    return data


async def get_child_to_parent(
        db: db_dependency,
        document_category: models.DocumentsCategories,
        contains_self: bool,
) -> ChildToParent:

    data = ChildToParent()

    result = []
    category_type = ""

    this = db.query(
        models.Categories
    ).where(
        models.Categories.Id == document_category.CategoryId
    ).first()

    if not this:
        raise HTTPException(403, "category not found!")

    result.append(category_data(this))

    if len(result) != 0:
        while result[-1].ParentId is not None:
            this = db.query(
                models.Categories
            ).where(
                models.Categories.Id == result[-1].ParentId
            ).first()
            if not this:
                raise HTTPException(403, "category not found!")
            result.append(category_data(this))
        else:
            category_type = result[-1].Type
        if not contains_self:
            del result[0]
        result.reverse()

    data.Id = document_category.Id
    data.Type = category_type
    data.Categories = result

    return data


async def get_parent_to_child_ids(
        db: db_dependency,
        category_id: int,
):
    result = []

    def get_ids(the_id: int):
        result.append(the_id)
        parent = db.query(
            models.Categories
        ).where(
            models.Categories.ParentId == the_id
        ).order_by(
            models.Categories.OrderBy.asc().nullslast(),
            models.Categories.Id.asc(),
        ).all()

        if not parent.__contains__(None):
            for i in parent:
                get_ids(i.Id)

    get_ids(category_id)
    return result
