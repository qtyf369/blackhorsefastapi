from pydantic import BaseModel, Field
from datetime import datetime


class FavouriteStatus(BaseModel):
    isFavorite: bool = True


class FavouriteResponse(BaseModel):
    id:  int
    user_id: int
    news_id: int
    created_at: datetime
