"""Node : juge la pertinence de tous les documents recuperes en un seul appel."""

from langchain_google_genai import ChatGoogleGenerativeAI

from supportiq.config import settings
from supportiq.graph.state import SupportState
from supportiq.schemas import GradeBatch

_PROMPT = """Tu evalues la pertinence de plusieurs documents pour un \
ticket de support client. Pour CHAQUE document numerote ci-dessous, \
indique s'il permet reellement de repondre au ticket. Reponds \
UNIQUEMENT sur la base du contenu fourni, sans supposer d'informations \
absentes. Tu dois retourner exactement un verdict par document, dans \
l'ordre ou tu le souhaites, en identifiant chacun par son index.

Ticket client :
{ticket}

Documents :
{documents}"""

_llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    google_api_key=settings.google_api_key,
).with_structured_output(GradeBatch)


def grade_documents(state: SupportState) -> dict:
    """Filtre les documents recuperes, ne garde que les pertinents."""
    docs = state["retrieved_docs"]

    if not docs:
        return {"relevant_docs": [], "grading_done": True}

    documents_text = "\n\n".join(
        f"[Document {i}]\n{doc.page_content}" for i, doc in enumerate(docs)
    )

    prompt = _PROMPT.format(ticket=state["ticket"], documents=documents_text)
    batch: GradeBatch = _llm.invoke(prompt)

    relevant_indices = {
        g.document_index for g in batch.grades if g.is_relevant
    }
    relevant = [doc for i, doc in enumerate(docs) if i in relevant_indices]

    return {"relevant_docs": relevant, "grading_done": True}