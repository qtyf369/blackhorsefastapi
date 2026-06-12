from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(msg: str = "success", data=None, ):
    content = {
        "code": 200,
        "message": msg,
        "data": data
    }
    # JSONResponse能自定义响应格式，如添加状态码、响应头等。status_code是HTTP状态码，成功默认200，但可根据需要自定义。
    # headers是响应头，如设置Content-Type为application/json。
    # 接口返回字典时，Fastapi会自动使用jsonable_encoder和JSONResponse。

    return JSONResponse(content=jsonable_encoder(content), status_code=200, headers={"Content-Type": "application/json"})
