from src.infra.context.app_context import AppContext
from src.infra.schemas.converter.converter_params import ConverterParams

def converter_params_depend() -> ConverterParams:
    return AppContext.converter_params
