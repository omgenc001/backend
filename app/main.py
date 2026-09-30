from fastapi import FastAPI
from settings.load_env import SQLALCHEMY_URL
from app.db.db_connections import Base, engine
from app.routes.auth import auth_router

dev_mode = FastAPI(title="Dev Mode")


@dev_mode.get("/")
def root():
    print(SQLALCHEMY_URL)
    return {"message": "Hello World"}


dev_mode.include_router(auth_router)
Base.metadata.create_all(bind=engine)

