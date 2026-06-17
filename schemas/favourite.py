from pydantic import BaseModel, Field


class FavouriteStatus(BaseModel):
    isFavorite: bool = True


class FavouriteResponse(BaseModel):
    data: FavouriteStatus = Field(default_factory=FavouriteStatus)
    # default_factory 被调用时，它会执行 FavouriteStatus(),这相当于每次创建 FavouriteResponse 时，data 字段都会得到一个全新的 FavouriteStatus实例，不会共享。
