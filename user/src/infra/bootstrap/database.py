from src.infra.database.postgresql.connection import init_postgresql_client, create_tables
from src.infra.database.mongodb.connection import init_mongodb_client
from src.infra.schemas.database.sqlalchemy import SqlalchemyParams, SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbParams, MongodbClient

async def init_postgresql(
    params: SqlalchemyParams,
) -> SqlalchemyClient:
    
    sql_client, engine = init_postgresql_client(
        host=params.host,
        port=params.port,
        username=params.username,
        password=params.password,
        db_name=params.db_name,
    )
    create_tables(engine)
    
    return SqlalchemyClient(
        params=params,
        client=sql_client,
        engine=engine,
    )

async def init_mongodb(
    params: MongodbParams,
) -> MongodbClient:
    
    mongo_client = await init_mongodb_client(
        host=params.host,
        port=params.port,
        username=params.username,
        password=params.password,
        db_name=params.db_name,
    )
    
    return MongodbClient(
        params=params,
        client=mongo_client,
    )

async def init_database_client(
    params: SqlalchemyParams | MongodbParams,
) -> SqlalchemyClient | MongodbClient:
    
    if isinstance(params, SqlalchemyClient):
        return await init_postgresql(params)
    elif isinstance(params, MongodbParams):
        return await init_mongodb(params)

async def terminate_database_client(
    context: SqlalchemyClient | MongodbClient | None = None,
):
    
    if not context:
        return
    
    if isinstance(context, SqlalchemyClient):
        context.client.close_all()       
        context.engine.dispose()
        
    if isinstance(context, MongodbClient):
        await context.client.close()
