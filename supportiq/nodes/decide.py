"""Node : applique les portes de decision booleennes, sans LLM."""

from langchain_core.documents import Document

from supportiq.graph.state import SupportState


def build_sources(docs: list[Document]) -> list[dict]:
    """Un element par document distinct, dans l'ordre de pertinence."""
    sources: dict[str, dict] = {}
    for doc in docs:
        doc_id = doc.metadata.get("doc_id")
        if doc_id not in sources:
            sources[doc_id] = {
                "doc_id": doc_id,
                "title": doc.metadata.get("title"),
                "source_type": doc.metadata.get("source_type"),
            }
    return list(sources.values())


def decide(state: SupportState) -> dict:
    """Decision finale : auto_response seulement si la reponse est ancree."""
    if state["is_grounded"]:
        return {
            "status": "auto_response",
            "sources": build_sources(state["relevant_docs"]),
        }
    return {"status": "human_review_required", "answer": None, "sources": []}