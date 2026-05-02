from abc import ABC, abstractmethod
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

class BaseBrokerClient(ABC):

    @abstractmethod
    def get_params_dependency(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_broker_dependency(self) -> RabbitBroker:
        raise NotImplementedError
    
    @abstractmethod
    def get_exchange_dependency(self) -> RabbitExchange:
        raise NotImplementedError
    
    @abstractmethod
    def get_queue_dependency(self) -> RabbitQueue:
        raise NotImplementedError
    