from pydantic import BaseModel, Field
from typing import List


class BannerModel(BaseModel):
    tag_ids: List[int] = Field(...)
    feature_id: int = Field(...)
    content: dict = Field(...)
    is_active: bool = Field(...)