"""Node : recherche les chunks les plus proches du ticket."""

from supportiq.graph.state import SupportState
from supportiq.rag.vector_store import get_vector_store


def retrieve(state: SupportState) -> dict:
    """Recherche les 4 chunks les plus proches du ticket."""
    docs = get_vector_store().similarity_search(state["ticket"], k=4)
    return {"retrieved_docs": docs}