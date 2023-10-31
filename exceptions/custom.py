from fastapi import HTTPException


class PasswordChangeError(HTTPException):
    def __init__(self, detail: str):
        status_code = 400
        super().__init__(status_code=status_code, detail=detail)


class PasswordMatchError(HTTPException):
    def __init__(self):
        status_code = 400
        detail = "Passwords do not match. Please make sure the new password and confirmation password are identical."
        super().__init__(status_code=status_code, detail=detail)
