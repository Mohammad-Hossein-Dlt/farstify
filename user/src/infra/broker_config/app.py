from faststream import FastStream
from .app_lifespan import lifespan

app = FastStream(
    lifespan=lifespan,
)