from fastapi import Depends
from src.infra.schemas.broker.broker_client import BaseBrokerClient
from src.worker.depends.broker_depend import broker_client_depend
from src.gateway.interface.Ibroker_service import IBrokerService
from src.gateway.rabbitmq.rabbitmq_service import RabbitMQService
from src.infra.schemas.broker.rabbitmq import RabbitClient

def convert_service_depend(
    client: BaseBrokerClient = Depends(broker_client_depend),
) -> IBrokerService:
    
    if isinstance(client, RabbitClient):
        return RabbitMQService(client)