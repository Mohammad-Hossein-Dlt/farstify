from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.context.context_manager import AppContextManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await AppContextManager.lazy_init_context()
                
    yield
    
    await AppContextManager.terminate_context()