from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.Idocument_repo import IDocumentRepo
from src.repo.mongodb.document_repo import DocumentMongodbRepo
   
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.repo.mongodb.document_image_repo import DocumentImageMongodbRepo
   
from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.repo.mongodb.document_link_repo import DocumentLinkMongodbRepo
   
def document_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentRepo:
    
    # if isinstance(db_client, Session):
    #     return DocumentMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentMongodbRepo()
   
def document_image_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentImageRepo:
    
    # if isinstance(db_client, Session):
    #     return DocumentImageMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentImageMongodbRepo()
    
def document_link_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentLinkRepo:
    
    # if isinstance(db_client, Session):
    #     return DocumentLinkMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentLinkMongodbRepo()
