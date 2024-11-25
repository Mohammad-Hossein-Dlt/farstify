from fastapi import HTTPException, status

owned_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="your are not owned this document",
    headers={"WWW-Authenticate": "forbidden"},
)