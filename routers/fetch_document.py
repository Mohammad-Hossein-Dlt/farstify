import models
from fastapi import APIRouter, status
from access_token import optional_user_token_dependency
from db_dependency import db_dependency
from constants import ContentTypes, SortBy, OrderBy
from actions.document_actions import get_document_short_info, get_document_full_info
from actions.categories_actions import get_parent_to_child_ids
from utills.check_follow import document_follow

router = APIRouter()


@router.get("/fetch-documents-by-category", status_code=status.HTTP_200_OK, tags=["FetchDocuments"])
async def fetch_documents_by_category(
        db: db_dependency,
        category_id: int,
        limit: int,
        page: int,
        sort_by: SortBy,
        order_by: OrderBy,
):
    result = []
    category = await get_parent_to_child_ids(db, category_id)
    docs = db.query(models.Document, models.Artists).select_from(
        models.DocumentsCategories
    ).order_by(
        models.Artists.Name.desc() if order_by is OrderBy.desc else models.Artists.Name.asc()
        if sort_by == SortBy.artist else
        models.Document.Name.desc() if order_by is OrderBy.desc else models.Document.Name.asc()
        if sort_by == SortBy.title else
        models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
    ).where(
        models.DocumentsCategories.CategoryId.in_(category)
    ).limit(limit).offset(limit * page).all()

    for document, artist in docs:
        result.append(await get_document_short_info(db=db, document=document, artist=artist))

    return result


@router.get("/fetch-documents", status_code=status.HTTP_200_OK, tags=["FetchDocuments"])
async def fetch_documents(
        db: db_dependency,
        content_type: ContentTypes,
        limit: int, page: int,
        sort_by: SortBy,
        order_by: OrderBy
):
    result = []

    docs = db.query(models.Document, models.Artists).join(
        models.Artists,
    ).order_by(
        models.Artists.Name.desc() if order_by is OrderBy.desc else models.Artists.Name.asc()
        if sort_by == SortBy.artist else
        models.Document.Name.desc() if order_by is OrderBy.desc else models.Document.Name.asc()
        if sort_by == SortBy.title else
        models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
    ).filter(
        models.Document.ContentType == content_type,
    ).limit(limit).offset(limit * page).all()

    for document, artist in docs:
        result.append(await get_document_short_info(db=db, document=document, artist=artist))

    return result


@router.get("/fetch-single-document", status_code=status.HTTP_200_OK, tags=["FetchDocuments"])
async def fetch_single_document(
        db: db_dependency,
        document_id: int,
        access_token: optional_user_token_dependency,
):
    document, artist = db.query(models.Document, models.Artists).join(
        models.Artists
    ).where(
        models.Document.Id == document_id
    ).first()

    if document and artist:
        document_info = await get_document_full_info(db=db, document=document, artist=artist)

        if access_token.permission:
            document_info.Followed = document_follow(db=db, user_id=access_token.user_id, document_id=document.Id)

        return document_info
