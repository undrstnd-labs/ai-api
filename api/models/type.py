from typing import List, Optional
from pydantic import BaseModel


class Model(BaseModel):
    id: str
    active: bool
    name: str
    description: str
    developer: str
    provider: str
    source: str
    tags: List[str]
    maxFileSize: Optional[int] = 4096
    maxContextWindow: Optional[int] = 4096 
    pricing: float
    inference: str


class TokenModelInference(BaseModel):
    model: Model
    inference: str
    token: str
