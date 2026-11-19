"""Contrat de l'API : ce que les guichets reçoivent et renvoient."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from supportiq.db.models import Role, TicketStatus

TicketText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=5000)
]


class TicketRequest(BaseModel):
    ticket: TicketText


class SourceItem(BaseModel):
    doc_id: str
    title: str | None = None
    source_type: str | None = None


class TicketOut(BaseModel):
    id: int
    text: str
    decision: str
    status: TicketStatus
    ai_answer: str | None
    sources: list[SourceItem]
    manager_reply: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SignupRequest(BaseModel):
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=255)
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=128)


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: Role

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut