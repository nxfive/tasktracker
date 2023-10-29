from fastapi import APIRouter
from routers import user, group, task, admin, label, board
from auth import authentication

router = APIRouter()

router.include_router(authentication.router)
router.include_router(user.router)
router.include_router(task.router)
router.include_router(group.router)
router.include_router(label.router)
router.include_router(board.router)
router.include_router(admin.router)
