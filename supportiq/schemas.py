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
    
class SingleGrade(BaseModel):
    """Verdict pour un document identifie par son index dans la liste envoyee."""

    document_index: int = Field(
        description="Index du document evalue, correspondant a son numero dans la liste fournie (commence a 0)."
    )
    is_relevant: bool = Field(
        description="Vrai si ce document aide reellement a repondre au ticket."
    )


class GradeBatch(BaseModel):
    """Verdicts pour l'ensemble des documents recuperes, en un seul appel."""

    grades: list[SingleGrade] = Field(
        description="Un verdict par document fourni, dans n'importe quel ordre, un seul par index."
    )
    
class AnswerValidation(BaseModel):
    """Verdict sur l'ancrage d'une reponse generee dans ses sources."""

    is_grounded: bool = Field(
        description=(
            "Vrai si TOUTES les affirmations de la reponse sont "
            "explicitement appuyees par les documents fournis. Faux si "
            "la reponse contient une information absente des documents."
        )
    )
    unsupported_claim: str | None = Field(
        default=None,
        description=(
            "Si is_grounded est faux, cite brievement l'affirmation "
            "problematique. Sinon, laisser vide."
        )
    )