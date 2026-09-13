"""Node : verifie que la reponse generee est ancree dans les sources."""

from langchain_google_genai import ChatGoogleGenerativeAI

from supportiq.config import settings
from supportiq.graph.state import SupportState
from supportiq.schemas import AnswerValidation

_PROMPT = """Tu verifies si une reponse de support client est \
entierement fondee sur les documents fournis, sans aucune information \
ajoutee, devinee ou extrapolee. Une reponse qui reformule ou resume \
fidelement le contenu des documents est consideree comme fondee, meme \
si elle n'utilise pas les memes mots.

Documents source :
{documents}

Reponse a verifier :
{answer}"""

_llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    google_api_key=settings.google_api_key,
).with_structured_output(AnswerValidation)


def validate_answer(state: SupportState) -> dict:
    """Verifie l'ancrage de la reponse, incremente le compteur de tentatives."""
    documents_text = "\n\n---\n\n".join(
        doc.page_content for doc in state["relevant_docs"]
    )

    prompt = _PROMPT.format(documents=documents_text, answer=state["answer"])
    verdict: AnswerValidation = _llm.invoke(prompt)

    return {
        "is_grounded": verdict.is_grounded,
        "generation_attempts": state["generation_attempts"] + 1,
    }