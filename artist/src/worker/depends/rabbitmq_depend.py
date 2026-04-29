from src.infra.context.app_context import AppContext
from faststream.rabbit import RabbitMessage
from functools import partial

def broker_client_depend():
    client = AppContext.broker_client
    return client

def target_routing_key(routing_key: str):
    def check(msg: RabbitMessage):
        return routing_key == msg.raw_message.routing_key
    
    return partial(check)