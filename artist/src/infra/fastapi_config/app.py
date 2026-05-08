import src
from .app_lifespan import lifespan
from fastapi import FastAPI
# from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_swagger import patch_fastapi
from pathlib import Path

BASE_DIR = Path(src.__file__).resolve().parent.parent

# from src.infra.middlewares.fastapi.logging_middleware import LoggingMiddleware
# from src.infra.middlewares.fastapi.prometheus_middleware import PrometheusMiddleware

# middlewares = [
    # Middleware(LoggingMiddleware),
    # Middleware(PrometheusMiddleware),
# ]

app: FastAPI = FastAPI(
    root_path="/artist-service",
    lifespan=lifespan,
    # middleware=middlewares,
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
) 

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static/lib", StaticFiles(directory=str(BASE_DIR / "static")), name="static_lib")

patch_fastapi(app, docs_url="")