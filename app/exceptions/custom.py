from fastapi import HTTPException


class PasswordChangeError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class PasswordMatchError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Passwords not match",
        )


class EntityNotExist(HTTPException):
    def __init__(self, entity: str):
        super().__init__(status_code=404, detail=f"{entity.title()} not found")


class PermissionDenied(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Access denied. No permission to perform this operation.",
        )
