import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.exception import PasswordError, UserNotFoundError
# 调试模式, 开发环境下开启, 生产环境下关闭
DEBUG = True
# 开发环境，返回详细错误信息

# 这里其实也可以不用异步函数，因为异常处理函数不需要异步操作，但Fastapi会自动调用异常处理函数，
# 保留了async def，后续方便异步操作，可以加


async def integrity_handler(request: Request, exc: IntegrityError):
    err_msg = str(exc.orig)
    # 判断具体错误类型
    if "username" in err_msg:
        err_msg = "用户名已存在"
    elif "foreign key" in err_msg.lower():
        err_msg = "关联数据不存在"
    else:
        err_msg = "数据重复或违反约束"

    err_data = None
    if DEBUG:
        err_data = {
            "error_type": 'IntegrityError',
            "detail": err_msg,
            'path': str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": err_msg, "data": err_data}
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    err_data = None
    if DEBUG:
        err_data = {
            "error_type": type(exc).__name__,
            "detail": str(exc),
            "path": str(request.url)
        }
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "数据库错误，请稍后重试", "data": err_data}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail}
    )


logger = logging.getLogger(__name__)  # 日志记录器


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": status.HTTP_404_NOT_FOUND, "message": "用户不存在"}
    )


async def password_error_handler(request: Request, exc: PasswordError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"code": status.HTTP_401_UNAUTHORIZED,
                 "message": str(exc) or "用户名密码错误"}
    )


async def generic_handler(request: Request, exc: Exception):
    print(">>> generic_handler 被调用了！")
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    err_data = None
    if DEBUG:
        err_data = {
            "error_type": type(exc).__name__,
            "detail": str(exc),
            "path": str(request.url)
        }
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误", "data": err_data}
    )
