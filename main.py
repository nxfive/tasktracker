from database.setup import Base, engine
from fastapi import FastAPI
from routers import user, group, task, label, board, admin
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(group.router)
app.include_router(label.router)
app.include_router(board.router)
app.include_router(admin.router)

Base.metadata.create_all(engine)

