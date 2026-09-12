"""Fonctions de routage : decident quel node executer ensuite."""

from typing import Literal

from supportiq.graph.state import SupportState


def route_after_grading(
    state: SupportState,
) -> Literal["generate_answer", "escalate"]:
    """S'il reste au moins un document pertinent, on genere ; sinon, on escalade."""
    if state["relevant_docs"]:
        return "generate_answer"
    return "escalate"