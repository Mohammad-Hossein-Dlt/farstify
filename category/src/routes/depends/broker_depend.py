from src.infra.context.app_context import AppContext

def broker_client_depend():
    client = AppContext.broker_client
    yield client
    
def broker_params_depend():
    client = AppContext.broker_client
    yield from client.get_params_dependency()
    
def broker_depend():
    client = AppContext.broker_client
    yield from client.get_broker_dependency()
    
def exchange_depend():
    client = AppContext.broker_client
    yield from client.get_exchange_dependency()
        
def queue_depend():
    client = AppContext.broker_client
    yield from client.get_queue_dependency()