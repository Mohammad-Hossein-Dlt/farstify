from fastapi import APIRouter

router = APIRouter(
    prefix="/upload-file",
    tags=["Upload File"]
)
