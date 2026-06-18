from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict


class userregister(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


# 封装返回体
class userInfoBase(BaseModel):  # 可选的基础信息，按需添加
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    gender: Optional[str] = Field(None, max_length=50, description="用户性别")
    bio: Optional[str] = Field(None, description="用户简介")
    avatar: Optional[str] = Field(None, description="用户头像")


class userInfoResponse(userInfoBase):  # 固定的基础信息，必填
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    model_config = ConfigDict(
        from_attributes=True)


class userDataResponse(BaseModel):  # 固定的基础信息，必填
    token: str = Field(..., description="用户令牌")
    user_info: userInfoResponse = Field(...,
                                        description="用户信息", alias="userInfo")
    # populate_by_name=True会让两个名字都兼容，默认输出别名
    model_config = ConfigDict(
        # from_attributes=True允许把ORM模型转换为Pydantic模型
        populate_by_name=True,
        from_attributes=True)


class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    gender: Optional[str] = Field(None, max_length=50, description="用户性别")
    bio: Optional[str] = Field(None, description="用户简介")
    avatar: Optional[str] = Field(None, description="用户头像")
    phone: Optional[str] = Field(None, max_length=11, description="用户手机号")


class UserPasswordUpdateRequest(BaseModel):
    new_password: str = Field(..., alias="newPassword", description="新密码")
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    model_config = ConfigDict(
        populate_by_name=True)
