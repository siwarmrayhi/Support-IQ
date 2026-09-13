"""Force un cas de non-ancrage pour verifier le cycle de regeneration."""

from langchain_core.documents import Document

from supportiq.nodes.validate import validate_answer

fake_state = {
    "relevant_docs": [
        Document(
            page_content="Le lien de reinitialisation est valable 30 minutes.",
            metadata={"doc_id": "auth_account_access"},
        )
    ],
    "answer": (
        "Le lien de reinitialisation est valable 24 heures et vous "
        "pouvez le renvoyer autant de fois que necessaire sans limite."
    ),
    "generation_attempts": 0,
}

result = validate_answer(fake_state)
print(f"is_grounded : {result['is_grounded']}")
print(f"tentatives  : {result['generation_attempts']}")