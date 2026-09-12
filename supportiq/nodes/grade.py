"""Node : juge la pertinence de chaque document recupere."""

from langchain_google_genai import ChatGoogleGenerativeAI

from supportiq.config import settings
from supportiq.graph.state import SupportState
from supportiq.schemas import DocumentGrade

_PROMPT = """Tu evalues si un document permet de repondre a un ticket \
de support client. Reponds UNIQUEMENT sur la base du contenu fourni, \
sans supposer d'informations absentes.

Ticket client :
{ticket}

Document a evaluer :
{document}"""

_llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    google_api_key=settings.google_api_key,
).with_structured_output(DocumentGrade)


def grade_documents(state: SupportState) -> dict:
    """Filtre les documents recuperes, ne garde que les pertinents."""
    relevant = []

    for doc in state["retrieved_docs"]:
        prompt = _PROMPT.format(ticket=state["ticket"], document=doc.page_content)
        grade: DocumentGrade = _llm.invoke(prompt)

        if grade.is_relevant:
            relevant.append(doc)

    return {"relevant_docs": relevant, "grading_done": True}