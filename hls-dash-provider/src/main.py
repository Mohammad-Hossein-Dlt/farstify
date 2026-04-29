from src.infra.context.app_context import AppContext
from src.infra.context.context_manager import AppContextManager

AppContextManager.init_context()

if AppContext.environment == 'dev':
    
    from src.infra.fastapi_config.app import app
    from src.routes.api_v1.main_router import main_router_v1
    
    app.include_router(main_router_v1)
    
elif AppContext.environment == 'test':
    
    from src.worker.consumer.app import app