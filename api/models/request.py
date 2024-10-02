from typing import List, Optional, Union
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "llama3-8b-8192"
    messages: List[Message] = None
    system: Optional[str] = None
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = 1
    logprobs: Optional[int] = None
    echo: Optional[bool] = False
    user: Optional[str] = None


class CompletionRequest(BaseModel):
    model: str = "llama3-8b-8192"
    prompt: str = None
    system: Optional[str] = None
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = 1
    logprobs: Optional[int] = None
    echo: Optional[bool] = False
    user: Optional[str] = None
