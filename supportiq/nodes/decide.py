"""Node : applique les portes de decision booleennes, sans LLM."""

from supportiq.graph.state import SupportState


def decide(state: SupportState) -> dict:
    """Decision finale : auto_response seulement si ancree ET pertinente."""
    if state["is_grounded"]:
        return {"status": "auto_response"}
    return {"status": "human_review_required", "answer": None}