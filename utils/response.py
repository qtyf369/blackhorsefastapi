from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas.users import userAuthResponse


def success_response(msg: str = "success", data=None, ):

    return userAuthResponse(code=200, message=msg, data=data)
