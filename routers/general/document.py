import models
from fastapi import APIRouter, status, HTTPException
from access_token import optional_user_token_dependency
from actions.episode_actions import get_episode_short_info
from db_dependency import db_dependency
from constants import ContentTypes, SortBy, OrderBy
from actions.document_actions import get_document_short_info, get_document_full_info
from actions.categories_actions import get_parent_to_child_ids
from utills.check_follow import document_follow, liked_episode

router = APIRouter(prefix="/document", tags=["General-Documents"])


@router.get("/fetch_documents_by_category", status_code=status.HTTP_200_OK)
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

    docs = db.query(
        models.Document,
        models.Artists
    ).select_from(
        models.DocumentsCategories
    ).order_by(
        models.Artists.Name.desc() if order_by is OrderBy.desc else models.Artists.Name.asc()
        if sort_by == SortBy.artist else
        models.Document.Name.desc() if order_by is OrderBy.desc else models.Document.Name.asc()
        if sort_by == SortBy.title else
        models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
    ).where(
        models.DocumentsCategories.CategoryId.in_(category)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for document, artist in docs:
        result.append(await get_document_short_info(db=db, document=document))

    return result


@router.get("/fetch_documents", status_code=status.HTTP_200_OK)
async def fetch_documents(
        db: db_dependency,
        content_type: ContentTypes,
        limit: int, page: int,
        sort_by: SortBy,
        order_by: OrderBy
):
    result = []

    docs = db.query(
        models.Document, models.Artists
    ).order_by(
        models.Artists.Name.desc() if order_by is OrderBy.desc else models.Artists.Name.asc()
        if sort_by == SortBy.artist else
        models.Document.Name.desc() if order_by is OrderBy.desc else models.Document.Name.asc()
        if sort_by == SortBy.title else
        models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
    ).filter(
        models.Document.ContentType == content_type
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for document, artist in docs:
        result.append(await get_document_short_info(db=db, document=document))

    return result


@router.get("/fetch_single_document", status_code=status.HTTP_200_OK)
async def fetch_single_document(
        db: db_dependency,
        document_id: int,
        access_token: optional_user_token_dependency,
):
    document = db.query(
        models.Document
    ).filter(
        models.Document.Id == document_id
    ).first()

    if not document:
        raise HTTPException(404, "document not found!")

    if document:
        document_info = await get_document_full_info(db=db, document=document)

        if access_token.permission:
            document_info.Followed = document_follow(db=db, user_id=access_token.user_id, document_id=document.Id)

        return document_info


@router.get("/fetch_all_episodes", status_code=status.HTTP_201_CREATED)
async def fetch_all_episodes(
        db: db_dependency,
        document_id: int,
        limit: int,
        page: int,
        access_token: optional_user_token_dependency,
):
    result = []

    episodes = db.query(
        models.DocumentsEpisodes
    ).where(
        models.DocumentsEpisodes.DocumentId == document_id
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    document = db.query(
        models.Document
    ).where(
        models.Document.Id == document_id
    ).first()

    if document is None:
        raise HTTPException(404, "document not found!")

    for i in episodes:
        episode = await get_episode_short_info(db=db, episode=i, document=document)

        if access_token.permission:
            episode.Followed = liked_episode(db=db, user_id=access_token.user_id, episode_id=episode.Id)

        result.append(episode)

    return result
