from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 封装密码加密函数


def hash_password(plain_password: str):
    return context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)
