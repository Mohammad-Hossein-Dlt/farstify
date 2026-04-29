from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_swagger import patch_fastapi
from .app_lifespan import lifespan

# from src.infra.middlewares.fastapi.logging_middleware import LoggingMiddleware
# from src.infra.middlewares.fastapi.prometheus_middleware import PrometheusMiddleware

# middlewares = [
    # Middleware(LoggingMiddleware),
    # Middleware(PrometheusMiddleware),
# ]

app: FastAPI = FastAPI(
    root_path="/converter-service",
    lifespan=lifespan,
    # middleware=middlewares,
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
) 

patch_fastapi(app,docs_url="")

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static/lib", StaticFiles(directory=str(BASE_DIR / "static")), name="static_lib")