from exceptions.custom import (
    PasswordChangeError,
    PasswordMatchError
)


class Validate:

    @staticmethod
    def validate_password_change(old: str, new: str, confirm: str):
        if new and not old:
            raise PasswordChangeError("Old password must be provided!")
        if new and not confirm:
            raise PasswordChangeError("Please confirm the password")
        else:
            if new != confirm:
                raise PasswordChangeError("Passwords are not the same")

    @staticmethod
    def validate_passwords_match(new: str, confirm: str):
        if new != confirm:
            raise PasswordMatchError
