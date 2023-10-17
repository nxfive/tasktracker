from database.setup import Base, engine
from fastapi import FastAPI
from routers import user
from auth import authentication

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)

Base.metadata.create_all(engine)

