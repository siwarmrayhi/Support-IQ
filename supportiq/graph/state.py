"""Etat partagé qui circule entre les nodes du graphe."""

from typing import TypedDict

from langchain_core.documents import Document


class SupportState(TypedDict):
    ticket: str
    retrieved_docs: list[Document]
    relevant_docs: list[Document]
    grading_done: bool