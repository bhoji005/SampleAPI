from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float = Field(ge=0)
    quantity: int = Field(default=0, ge=0)


class ItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    quantity: int
    created_at: datetime
    updated_at: datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
