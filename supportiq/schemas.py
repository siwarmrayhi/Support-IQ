"""Schemas Pydantic pour les sorties structurees des appels LLM."""

from pydantic import BaseModel, Field


class DocumentGrade(BaseModel):
    """Jugement de pertinence pour un seul document face a un ticket."""

    is_relevant: bool = Field(
        description="Vrai si ce document aide reellement a repondre au ticket."
    )
    reason: str = Field(
        description="Justification breve du jugement, une phrase maximum."
    )