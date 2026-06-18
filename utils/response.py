from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas.common import ApiResponse


def success_response(msg: str = "success", data=None):

    return ApiResponse(code=200, message=msg, data=data)
