from database.setup import Base, engine
from fastapi import FastAPI
from routers import user, group, task
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(group.router)

Base.metadata.create_all(engine)

