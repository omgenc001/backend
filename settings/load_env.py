import os
from pathlib import Path
from dotenv import load_dotenv


path = __file__

BASE_DIR = Path(path).resolve().parent.parent

env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

SQLALCHEMY_URL = os.getenv("SQLALCHEMY_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TIME = os.getenv("ACCESS_TIME")