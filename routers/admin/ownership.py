from typing import List
import models
from actions.ownerships_actions import get_ownership_info
from actions.raw_artist_info_actions import get_raw_artist_info
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from actions.response_model import ResponseMessage

router = APIRouter(prefix="/admin/ownership", tags=["Admin-Ownership"])


@router.get("/fetch_ownerships", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        document_id: int,
):
    ownerships = db.query(
        models.Artists,
        models.DocumentsOwners,
    ).join(
        models.DocumentsOwners
    ).where(
        models.DocumentsOwners.DocumentId == document_id,
    ).order_by(
        models.DocumentsOwners.OrderBy.asc().nullslast(),
        models.DocumentsOwners.Id.asc(),
    ).all()

    return [
        get_ownership_info(db=db, ownership=ownership, artist=artist)
        for artist, ownership in ownerships
    ]


@router.post("/insert_ownership", status_code=status.HTTP_200_OK)
async def insert_agent(
        db: db_dependency,
        artist_id: int,
        document_id: int,
):
    artist = db.query(models.Artists).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, f"admin not found!")

    document = db.query(
        models.Document
    ).where(
        models.Document.Id == document_id
    ).first()

    if not artist:
        raise HTTPException(404, f"document not found!")

    ownership = db.query(
        models.DocumentsOwners
    ).where(
        models.DocumentsOwners.ArtistId == artist.Id,
        models.DocumentsOwners.DocumentId == document.Id,
    ).first()

    if ownership:
        raise HTTPException(403, f"{artist.Name} already owns this document")

    ownership = models.DocumentsOwners()
    ownership.ArtistId = artist_id
    ownership.DocumentId = document_id

    db.add(ownership)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'ownership has been added',
        },
    )


@router.put("/reorder_ownerships", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        document_id: int,
        ownerships_ids: List[int],
):
    ownerships = db.query(
        models.DocumentsOwners
    ).where(
        models.DocumentsOwners.DocumentId == document_id,
    ).all()

    for index, ownership_id in enumerate(ownerships_ids):
        for ownership in ownerships:
            if ownership.Id == ownership_id:
                ownership.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'ownerships has been reordered',
        },
    )


@router.delete("/delete_ownership", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        ownership_id: int,
):
    ownership = db.query(models.DocumentsOwners).where(
        models.DocumentsOwners.Id == ownership_id,
    ).first()

    if not ownership:
        raise HTTPException(404, "ownership not found!")

    artist = db.query(models.Artists).where(
        models.Artists.Id == ownership.Id
    ).first()

    db.delete(ownership)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': f'{artist.Name} was deleted from the owners of this document',
        },
    )
