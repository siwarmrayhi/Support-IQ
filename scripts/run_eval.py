"""Évalue le retrieval sur le dataset annoté et affiche le recall@k."""

import json

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings
from supportiq.eval_metrics import EvalReport, TicketResult

K = 4


def load_dataset() -> list[dict]:
    """Lit eval/dataset.jsonl, une ligne = un ticket."""
    path = settings.raw_data_dir.parent.parent / "eval" / "dataset.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_vector_store() -> Chroma:
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )
    return Chroma(
        persist_directory=str(settings.index_dir),
        embedding_function=embeddings,
        collection_name="supportiq",
    )


def retrieve_doc_ids(store: Chroma, query: str, k: int) -> list[str]:
    """Retourne les doc_id des k chunks les plus proches, sans doublon."""
    results = store.similarity_search(query, k=k)
    seen = []
    for doc in results:
        doc_id = doc.metadata.get("doc_id")
        if doc_id not in seen:
            seen.append(doc_id)
    return seen


def run() -> None:
    tickets = load_dataset()
    store = load_vector_store()
    report = EvalReport()

    for ticket in tickets:
        expected = ticket["relevant_doc_ids"]
        if not expected:
            continue  # cas de refus : pas de recall à mesurer ici

        retrieved = retrieve_doc_ids(store, ticket["ticket"], k=K)

        result = TicketResult(
            ticket_id=ticket["id"],
            expected_doc_ids=expected,
            retrieved_doc_ids=retrieved,
            has_exact_identifier=ticket["has_exact_identifier"],
        )
        report.results.append(result)

        status = "OK  " if result.is_full_hit else "MISS"
        print(f"[{status}] {ticket['id']:6s} attendu={expected} trouvé={retrieved}")

    print(f"\nTickets évalués (hors refus) : {len(report.results)}")
    print(f"Recall@{K} global              : {report.recall_at_k():.1%}")
    print(f"Recall@{K} avec identifiant     : {report.recall_at_k(report.with_identifier):.1%}")
    print(f"Recall@{K} sans identifiant     : {report.recall_at_k(report.without_identifier):.1%}")
    print(f"MRR global                     : {report.mrr():.3f}")
    print(f"MRR avec identifiant            : {report.mrr(report.with_identifier):.3f}")


if __name__ == "__main__":
    run()