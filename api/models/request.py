from typing import Any, List, Optional, Union

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = None
    logprobs: Optional[bool] = None
    user: Optional[str] = None


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = None
    logprobs: Optional[bool] = None
    user: Optional[str] = None


class ChatRequestRAG(BaseModel):
    model: str
    messages: List[Message]
    dataSourceToken: str
    similarityLength: Optional[int] = 5
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = None
    logprobs: Optional[bool] = None
    user: Optional[str] = None


class CompletionRequestRAG(BaseModel):
    model: str
    prompt: str
    dataSourceToken: str
    similarityLength: Optional[int] = 5
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = None
    logprobs: Optional[bool] = None
    user: Optional[str] = None


class AudioTranscriptions(BaseModel):
    file: Any
    model: str
    prompt: Optional[str] = None
    response_format: Optional[str] = None
    temperature: Optional[float] = None
    language: Optional[str] = None


class AudioTranslations(BaseModel):
    file: Any
    model: str
    prompt: Optional[str]
    response_format: Optional[str]
    temperature: Optional[float]
