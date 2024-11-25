import models
from fastapi import APIRouter, status
from db_dependency import db_dependency
from constants import ContentTypes, SortBy, OrderBy
from typing import List

router = APIRouter()

async def clean_up_documentsId(
        db: db_dependency,
        documents_id: list,
) -> list:
    return [x for x in documents_id if len(db.query(models.Document).where(models.Document.Id == x).all()) == 1]


@router.post("/insert-home-page-item", status_code=status.HTTP_201_CREATED, tags=["Homepage"])
async def insert_home_page_item(
        db: db_dependency,
        title: str,
        content_types: ContentTypes,
        sorted_by: SortBy,
        order_by: OrderBy,
        category_id: int | None = None,
        documents_id: List[int] | None = None,
):
    item = models.HomePageItems()
    item.Title = title
    item.Type = content_types
    item.SortedBy = sorted_by
    item.OrderBy = order_by
    item.CategoryId = category_id
    db.add(item)
    db.commit()

    if documents_id is not None and len(documents_id) != 0:
        documents = await clean_up_documentsId(db, documents_id)
        for i in documents:
            category = models.HomePageDocumentsRepository(**{"DocumentId": i, "HomePageItemId": item.Id})
            db.add(category)

    db.commit()


@router.put("/update-home-page-item", status_code=status.HTTP_200_OK, tags=["Homepage"])
async def update_home_page_item(
        db: db_dependency,
        item_id: int,
        title: str | None = None,
        page: ContentTypes | None = None,
        sorted_by: SortBy | None = None,
        order_by: OrderBy | None = None,
        category_id: int | None = None,
        documents_id: List[int] | None = None,
):
    the_item = db.query(models.HomePageItems).where(models.HomePageItems.Id == item_id).first()

    if the_item is not None:
        the_item.Title = title if title is not None else the_item.Title
        the_item.ContentType = page if page is not None else the_item.ContentType
        the_item.SortedBy = sorted_by if sorted_by is not None else the_item.SortedBy
        the_item.OrderBy = order_by if order_by is not None else the_item.OrderBy
        the_item.CategoryId = category_id if category_id is not None else the_item.CategoryId

        if documents_id is not None and len(documents_id) != 0:
            delete = db.query(models.HomePageDocumentsRepository).where(
                models.HomePageDocumentsRepository.HomePageItemId == item_id).all()
            for i in delete:
                db.delete(i)
            documents = await clean_up_documentsId(db, documents_id)
            for i in documents:
                category = models.HomePageDocumentsRepository(**{"DocumentId": i, "HomePageItemId": item_id})
                db.add(category)

    db.commit()


@router.delete("/delete-home-page-item", status_code=status.HTTP_201_CREATED, tags=["Homepage"])
async def delete_home_page_item(
        db: db_dependency,
        item_id: int,
):
    item = db.query(models.HomePageItems).where(models.HomePageItems.Id == item_id).first()
    if item:
        db.delete(item)
        db.commit()


@router.get("/fetch-home-page", status_code=status.HTTP_200_OK, tags=["Homepage"])
async def fetch_home_page(
        db: db_dependency,
        content_types: ContentTypes,
        limit: int,
        page: int,
):
    items = db.query(models.HomePageItems).where(
        models.HomePageItems.Type == content_types,
    ).limit(limit).offset(limit * page).all()

    for i in items:
        x = db.query(models.HomePageDocumentsRepository, models.Document).join(models.Document).where(
            models.HomePageDocumentsRepository.HomePageItemId == i.Id).first()

    return items
