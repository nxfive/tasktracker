from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes="bcrypt", deprecated="auto")


class Hash:

    @staticmethod
    def bcrypt(password: str):
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        return pwd_ctx.verify(secret=plain_password, hash=hashed_password)
