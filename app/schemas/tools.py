class Validate:
    @staticmethod
    def validate_password_change(old: str, new: str, confirm: str):
        if new and not old:
            raise ValueError("Old password must be provided!")
        if new and not confirm:
            raise ValueError("Please confirm the password")
        else:
            if new != confirm:
                raise ValueError("Passwords are not the same")

    @staticmethod
    def validate_passwords_match(new: str, confirm: str):
        if new != confirm:
            raise ValueError("Passwords do not match")
