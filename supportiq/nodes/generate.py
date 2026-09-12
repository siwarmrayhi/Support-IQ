"""Node : genere une reponse basee uniquement sur les documents pertinents."""

from langchain_google_genai import ChatGoogleGenerativeAI

from supportiq.config import settings
from supportiq.graph.state import SupportState

_PROMPT = """Tu es un assistant de support client pour CloudDesk. \
Redige une reponse professionnelle et concise au ticket ci-dessous, \
en te basant UNIQUEMENT sur les documents fournis. N'invente aucune \
information absente des documents. Si les documents ne couvrent pas \
completement la question, dis-le explicitement dans ta reponse.

Ticket client :
{ticket}

Documents disponibles :
{documents}

Reponse :"""

_llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    google_api_key=settings.google_api_key,
)


def generate_answer(state: SupportState) -> dict:
    """Genere une reponse ancree dans les documents juges pertinents."""
    documents_text = "\n\n---\n\n".join(
        f"[{doc.metadata.get('doc_id')}] {doc.page_content}"
        for doc in state["relevant_docs"]
    )

    prompt = _PROMPT.format(ticket=state["ticket"], documents=documents_text)
    response = _llm.invoke(prompt)

    return {"answer": response.text.strip(), "status": "auto_response"}