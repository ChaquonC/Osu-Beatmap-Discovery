from pydantic import BaseModel
from typing import Callable

class Tool(BaseModel):
    fn: Callable
    name: str
    description: str
    tags: set
    metadata: dict