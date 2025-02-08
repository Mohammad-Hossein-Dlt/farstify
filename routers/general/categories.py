import models
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from constants import ContentTypes
from actions.categories_actions import category_data
from utills.parse_null import pars_null

router = APIRouter(prefix="/category", tags=["General-Category"])


@router.get("/fetch_categories", status_code=status.HTTP_200_OK)
async def fetch_categories(
        db: db_dependency,
        category_type: ContentTypes,
        parent_id: str | None = None,
        contains_child: bool = False,
):
    parent_id = pars_null(parent_id)

    result = []

    parents = db.query(
        models.Categories
    ).where(
        models.Categories.ParentId == parent_id,
        models.Categories.Type == category_type,
    ).order_by(
        models.Categories.OrderBy.asc().nullslast(),
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
