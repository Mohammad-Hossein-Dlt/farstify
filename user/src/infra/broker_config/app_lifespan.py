from faststream import ContextRepo
from contextlib import asynccontextmanager
from src.infra.context.context_manager import AppContextManager

@asynccontextmanager
async def lifespan(app: ContextRepo):
    
    await AppContextManager.lazy_init_context()
                
    yield
    
    await AppContextManager.terminate_context()