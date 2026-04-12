from pydantic import BaseModel
from typing import Optional


class MyAction(BaseModel):
    action: str  # e.g. "image.png -> images"


class MyObservation(BaseModel):
    files: list[str]
    message: Optional[str] = None
    reward: Optional[float] = None
    done: bool = False
