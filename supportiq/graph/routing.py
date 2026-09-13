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


MAX_GENERATION_ATTEMPTS = 2

def route_after_validation(
    state: SupportState,
) -> Literal["decide", "generate_answer"]:
    """Si ancree, on termine. Sinon, une seule regeneration, puis on abandonne."""
    if state["is_grounded"]:
        return "decide"
    if state["generation_attempts"] < MAX_GENERATION_ATTEMPTS:
        return "generate_answer"
    return "decide"