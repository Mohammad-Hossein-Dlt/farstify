from typing import List

import models
from db_dependency import db_dependency
from fastapi import APIRouter, status, HTTPException
from actions.response_model import ResponseMessage

router = APIRouter(prefix="/ownership", tags=["Ownership"])


@router.post("/add_ownership", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        artist_id: int,
        document_id: int,
):
    artist = db.query(models.Artists).where(
        models.Artists.Id == artist_id
    ).first()

    if not artist:
        raise HTTPException(404, f"artist not found!")

    ownership = db.query(
        models.DocumentsOwners
    ).where(
        models.DocumentsOwners.ArtistId == artist.Id,
        models.DocumentsOwners.DocumentId == document_id,
    ).first()

    if ownership:
        raise HTTPException(403, f"{artist.Name} already owns this document.")

    ownership = models.DocumentsOwners()
    ownership.ArtistId = artist_id
    ownership.DocumentId = document_id

    db.add(ownership)
    db.commit()
    return ResponseMessage(error=False, message="ownerships has been added.")


@router.put("/reorder_ownership", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        document_id: int,
        roles_ids: List[int],
):
    ownerships = db.query(
        models.DocumentsOwners
    ).where(
        models.DocumentsOwners.DocumentId == document_id,
    ).all()

    for index, ownership_id in enumerate(roles_ids):
        for ownership in ownerships:
            if ownership.Id == ownership_id:
                ownership.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message="ownerships has been reordered.")


@router.post("/fetch_ownership", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        document_id: int,
):
    ownership = db.query(models.DocumentsOwners).where(
        models.DocumentsOwners.DocumentId == document_id,
    ).all()

    return ownership


@router.post("/delete_ownership", status_code=status.HTTP_200_OK)
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
    return ResponseMessage(error=False, message=f"{artist.Name} was deleted from the owners of this document.")
