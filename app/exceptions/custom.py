from fastapi import HTTPException


class PasswordChangeError(Exception):
    def __init__(self, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class PasswordMatchError(Exception):
    def __init__(self):
        status_code = 400
        detail = "Passwords do not match. Please make sure the new password and confirmation password are identical."
        super().__init__(status_code=status_code, detail=detail)
