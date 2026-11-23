"""Recherche, filtres et statistiques sur les tickets (sans dépendance à Streamlit)."""

import unicodedata

STATUS_FILTERS = {
    "Tous": None,
    "À traiter": "pending_review",
    "En cours": "in_progress",
    "Terminé": "resolved",
}


def normalize(text: str) -> str:
    """Minuscules et sans accents, pour une recherche tolérante."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def filter_tickets(tickets: list[dict], query: str = "", status: str | None = None) -> list[dict]:
    """Garde les tickets qui contiennent tous les mots de la recherche."""
    words = normalize(query).split()
    results = []
    for ticket in tickets:
        if status and ticket["status"] != status:
            continue
        haystack = normalize(
            " ".join(
                [
                    f"#{ticket['id']}",
                    ticket["text"],
                    ticket.get("ai_answer") or "",
                    ticket.get("manager_reply") or "",
                ]
            )
        )
        if all(word in haystack for word in words):
            results.append(ticket)
    return results


def compute_stats(tickets: list[dict]) -> dict:
    total = len(tickets)
    auto = sum(t["decision"] == "auto_response" for t in tickets)
    return {
        "total": total,
        "resolved": sum(t["status"] == "resolved" for t in tickets),
        "in_progress": sum(t["status"] == "in_progress" for t in tickets),
        "pending": sum(t["status"] == "pending_review" for t in tickets),
        "auto": auto,
        "auto_rate": round(100 * auto / total) if total else 0,
    }


def shorten(text: str, limit: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"