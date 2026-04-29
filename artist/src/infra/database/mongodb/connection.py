from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .collections.artist_collection import ArtistCollection
from .collections.artist_image_collection import ArtistImageCollection
from .collections.artist_link_collection import ArtistLinkCollection
from beanie import init_beanie


async def init_mongodb_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncMongoClient:
    
    client = AsyncMongoClient(
        host=host,
        port=port,
        username=username,
        password=password,
    )
    
    database = AsyncDatabase(
        client=client,
        name=db_name,
    )
    
    await init_beanie(
        database=database,
        document_models=[
            ArtistCollection,
            ArtistImageCollection,
            ArtistLinkCollection,
        ],
    )
    
    return client