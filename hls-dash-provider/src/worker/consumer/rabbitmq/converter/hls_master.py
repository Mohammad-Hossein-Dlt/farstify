from faststream import Depends
from src.worker.consumer.rabbitmq.broker import subscriber
from src.worker.depends.rabbitmq_depend import target_routing_key
from faststream.rabbit import RabbitMessage
from src.infra.schemas.converter.converter_params import ConverterParams
from src.worker.depends.converter_depend import converter_params_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.worker.depends.storage_depend import storage_repo_depend
from src.repo.interface.Icache import ICacheRepo
from src.worker.depends.cache_depend import cache_repo_depend
from src.gateway.interface.Ibroker_service import IBrokerService
from src.worker.depends.services_depend import convert_service_depend
from src.usecases.converter.hls_master import CreateHlsMaster
from src.infra.exceptions.exceptions import AppBaseException

routing_key = "audio.hls.master.create"

@subscriber(
    filter=target_routing_key(routing_key),
)
async def create_hls_master(
    msg: RabbitMessage,
    object_name: str,
    converter_params: ConverterParams = Depends(converter_params_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    broker_service: IBrokerService = Depends(convert_service_depend),
):
    try:

        dash_converter_usecase = CreateHlsMaster(converter_params, storage_repo, cache_repo, broker_service)
        await dash_converter_usecase.execute(object_name)
        
    except AppBaseException as ex:
        await msg.reject(requeue=False)
        return ex.model_dump()
    except Exception as ex:
        await msg.reject(requeue=False)
        return AppBaseException(status_code=500, message="Error....").model_dump()
