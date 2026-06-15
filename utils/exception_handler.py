async def exception_handler(app):
    """
    异常处理函数
    """
    from utils.exception import (
        integrity_handler,
        sqlalchemy_error_handler,
        http_exception_handler,
        generic_handler
    )
    """
    异常处理函数
    """
    app.add_exception_handler(IntegrityError, integrity_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_handler)
