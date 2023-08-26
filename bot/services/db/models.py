from pydantic import BaseModel, Field
from typing import Optional


class Settings(BaseModel):
    history: list[dict[str, str]]
    prompt: str
    temperature: float = Field(None, alias="model_temperature")


class OSettings(BaseModel):
    history: Optional[list[dict[str, str]]] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = Field(None, alias="model_temperature")


class User(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    settings: Optional[OSettings] = None
    collection: Optional["Collection"] = None


class OUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    settings: Optional[OSettings] = None
    collection: Optional["Collection"] = None


class Collection(BaseModel):

    dir_id: Optional[str] = None
    documents: Optional[list[str]] = None
    user: Optional[User] = None
