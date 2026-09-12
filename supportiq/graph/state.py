"""Etat partagé qui circule entre les nodes du graphe."""

from typing import Literal, TypedDict

from langchain_core.documents import Document


class SupportState(TypedDict):
    ticket: str
    retrieved_docs: list[Document]
    relevant_docs: list[Document]
    grading_done: bool
    answer: str | None
    status: Literal["auto_response", "human_review_required"] | None