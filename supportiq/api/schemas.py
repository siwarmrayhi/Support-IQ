"""Contrat de l'API : ce que le guichet reçoit et ce qu'il renvoie."""

from typing import Literal

from pydantic import BaseModel, Field


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