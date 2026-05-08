import src
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(src.__file__).resolve().parent.parent

is_production = "/app" in str(BASE_DIR)

if is_production:
    templates = Jinja2Templates(directory=BASE_DIR / "./templates")
else:
    templates = Jinja2Templates(directory=BASE_DIR / "./templates")
