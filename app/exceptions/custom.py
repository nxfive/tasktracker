from fastapi import HTTPException


class EntityNotExist(HTTPException):
    def __init__(self, entity: str):
        super().__init__(status_code=404, detail=f"{entity.title()} not found")


class PermissionDenied(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Access denied. No permission to perform this operation.",
        )
