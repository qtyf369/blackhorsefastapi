from pydantic import BaseModel, Field

from typing import Generic, TypeVar
# 定义泛型类型变量
T = TypeVar("T")


# 封装返回体,泛型T
class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="状态描述")
    data: T | None = Field(None, description="数据")
