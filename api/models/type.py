from enum import Enum
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


class StatusEnum(str, Enum):
    FAILED = "FAILED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"


class Request(BaseModel):
    id: str
    status: StatusEnum
    parameters: dict
    request: dict
    response: str
    endpoint: str
    user_id: str
    apiTokenId: str
