from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.exception import  PasswordError, UserNotFoundError


def exception_handler(app):
    """
    异常处理函数
    """
    from utils.exception import (
        integrity_handler,
        sqlalchemy_error_handler,
        http_exception_handler,
        generic_handler,
        user_not_found_handler,
        password_error_handler
    )
    """
    异常处理函数
    """
    app.add_exception_handler(IntegrityError, integrity_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(PasswordError, password_error_handler)
    app.add_exception_handler(Exception, generic_handler)
