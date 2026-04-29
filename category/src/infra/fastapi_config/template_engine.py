from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
is_production = "/app" in str(BASE_DIR)

if is_production:
    templates = Jinja2Templates(directory=BASE_DIR / "./templates")
else:
    templates = Jinja2Templates(directory=BASE_DIR / "./templates")
