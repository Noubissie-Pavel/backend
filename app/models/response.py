from typing import List, Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int


class ResponseModel(BaseModel):
    metadata: Optional[Metadata] = None
    status: int
    message: str
    data: List
