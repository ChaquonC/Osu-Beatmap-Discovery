from pydantic import BaseModel
from typing import Any


class APIResponseModel(BaseModel):
    ok: bool
    data: Any
