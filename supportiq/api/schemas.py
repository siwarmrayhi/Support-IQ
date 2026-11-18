"""Contrat de l'API : ce que le guichet reçoit et ce qu'il renvoie."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from supportiq.db.models import Role


class TicketRequest(BaseModel):
    ticket: str = Field(min_length=1, max_length=5000)


class SourceItem(BaseModel):
    doc_id: str
    title: str | None = None
    source_type: str | None = None


class TicketResponse(BaseModel):
    status: Literal["auto_response", "human_review_required"]
    answer: str | None
    sources: list[SourceItem]
    
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