from pydantic import BaseModel
from typing import Any


class APIResponseModel(BaseModel):
    status_code: int
    data: Any
