from fastapi import APIRouter

router = APIRouter(
    prefix="/play",
    tags=["Play audio"]
)
