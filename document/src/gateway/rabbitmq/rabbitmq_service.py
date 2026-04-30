from src.gateway.interface.Ibroker_service import IBrokerService
from src.infra.schemas.broker.rabbitmq import RabbitClient
from src.domain.enums import Format
from src.infra.exceptions.exceptions import AppBaseException


class RabbitMQService(IBrokerService):
    
    def __init__(
        self,
        client: RabbitClient,
    ):
        self.client = client
    
    async def convert(
        self,
        object_name: str,
        format: Format,
    ) -> bool:
        
        try:
            
            if format == "dash":
                await self.client.broker.publish(
                    message=object_name,
                    exchange=self.client.exchange,
                    routing_key="audio.dash.convert",
                )
            elif format == "hls":
                await self.client.broker.publish(
                    message=object_name,
                    exchange=self.client.exchange,
                    routing_key="audio.hls.convert",
                )
            
            return True
        except:
            return False
            
    async def create_stream_file(
        self,
        object_name: str,
        format: Format,
    ) -> bool:
        
        try:
            
            if format == "dash":
                await self.client.broker.publish(
                    message=object_name,
                    exchange=self.client.exchange,
                    routing_key="audio.dash.manifest.create",
                )
            elif format == "hls":
                await self.client.broker.publish(
                    message=object_name,
                    exchange=self.client.exchange,
                    routing_key="audio.hls.master.create",
                )
            
            return True
        except:
            return False