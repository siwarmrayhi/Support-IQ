"""Tests de la recherche, des filtres et des statistiques (aucune base, aucun LLM)."""

from ui.ticket_utils import compute_stats, filter_tickets, normalize, shorten


def make(id, text, status="resolved", decision="auto_response", ai_answer=None, manager_reply=None):
    return {
        "id": id,
        "text": text,
        "status": status,
        "decision": decision,
        "ai_answer": ai_answer,
        "manager_reply": manager_reply,
    }


def test_normalize_retire_accents_et_majuscules():
    assert normalize("Réinitialiser À L'ÉCOLE") == "reinitialiser a l'ecole"


def test_recherche_ignore_accents_et_casse():
    tickets = [make(1, "J'ai oublié mon mot de passe")]
    assert filter_tickets(tickets, "OUBLIE") == tickets


def test_recherche_exige_tous_les_mots():
    tickets = [make(1, "mot de passe oublié"), make(2, "paiement échelonné")]
    assert filter_tickets(tickets, "mot paiement") == []
    assert filter_tickets(tickets, "mot passe") == [tickets[0]]


def test_recherche_par_numero():
    tickets = [make(3, "bonjour"), make(4, "autre")]
    assert filter_tickets(tickets, "#3") == [tickets[0]]


def test_recherche_dans_les_reponses():
    tickets = [make(1, "question", ai_answer="Le lien est valable 30 minutes")]
    assert filter_tickets(tickets, "30 minutes") == tickets


def test_filtre_par_statut():
    tickets = [make(1, "a", status="resolved"), make(2, "b", status="pending_review")]
    assert filter_tickets(tickets, "", "pending_review") == [tickets[1]]


def test_requete_vide_renvoie_tout():
    tickets = [make(1, "a"), make(2, "b")]
    assert filter_tickets(tickets, "   ") == tickets


def test_statistiques():
    tickets = [
        make(1, "a"),
        make(2, "b", status="pending_review", decision="human_review_required"),
        make(3, "c", status="in_progress", decision="human_review_required"),
        make(4, "d"),
    ]
    assert compute_stats(tickets) == {
        "total": 4,
        "resolved": 2,
        "in_progress": 1,
        "pending": 1,
        "auto": 2,
        "auto_rate": 50,
    }


def test_statistiques_sans_ticket():
    assert compute_stats([])["auto_rate"] == 0


def test_shorten():
    assert shorten("a  b\nc", 10) == "a b c"
    assert shorten("x" * 100, 10) == "x" * 9 + "…"