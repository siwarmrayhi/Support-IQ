"""Node : prepare l'escalade vers un agent humain."""

from supportiq.graph.state import SupportState


def escalate(state: SupportState) -> dict:
    """Aucun document pertinent : le systeme ne doit pas inventer de reponse."""
    return {
        "answer": None,
        "status": "human_review_required",
    }