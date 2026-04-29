from src.infra.context.app_context import AppContext

def db_client_depend():
    client = AppContext.db_client
    yield from client.get_dependency()