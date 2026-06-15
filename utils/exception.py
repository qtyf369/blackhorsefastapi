import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# 调试模式, 开发环境下开启, 生产环境下关闭
DEBUG = True
# 开发环境，返回详细错误信息


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


async def generic_handler(request: Request, exc: Exception):
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
