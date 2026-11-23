"""Tests des routes du gestionnaire (base en mémoire, aucun LLM)."""

from supportiq.db.models import TicketStatus
from tests.helpers import add_ticket, create_client_account, create_manager_account


def status_path(ticket_id):
    return f"/manager/tickets/{ticket_id}/status"


def reply_path(ticket_id):
    return f"/manager/tickets/{ticket_id}/reply"


def test_liste_sans_jeton_est_refusee(client):
    assert client.get("/manager/tickets").status_code == 401


def test_un_client_ne_peut_pas_utiliser_les_routes_du_gestionnaire(client):
    _, headers = create_client_account(client)
    assert client.get("/manager/tickets", headers=headers).status_code == 403


def test_le_gestionnaire_voit_les_tickets_de_tous_les_clients(client, session_factory):
    id_a, _ = create_client_account(client, "a@example.com", "Alice")
    id_b, _ = create_client_account(client, "b@example.com", "Bob")
    add_ticket(session_factory, id_a, "premier")
    add_ticket(session_factory, id_b, "second")
    headers = create_manager_account(client, session_factory)

    body = client.get("/manager/tickets", headers=headers).json()
    assert [t["text"] for t in body] == ["second", "premier"]
    assert body[0]["client_name"] == "Bob"
    assert body[1]["client_email"] == "a@example.com"


def test_filtre_par_statut(client, session_factory):
    client_id, _ = create_client_account(client)
    add_ticket(session_factory, client_id, "a traiter")
    add_ticket(
        session_factory,
        client_id,
        "termine",
        status=TicketStatus.resolved,
        decision="auto_response",
        ai_answer="ok",
    )
    headers = create_manager_account(client, session_factory)

    body = client.get("/manager/tickets?status=resolved", headers=headers).json()
    assert [t["text"] for t in body] == ["termine"]


def test_prise_en_charge(client, session_factory):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory, name="Agent Un")

    response = client.patch(
        status_path(ticket_id), json={"status": "in_progress"}, headers=headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["assigned_to_name"] == "Agent Un"


def test_remise_en_a_traiter_efface_l_affectation(client, session_factory):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory)
    client.patch(status_path(ticket_id), json={"status": "in_progress"}, headers=headers)

    response = client.patch(
        status_path(ticket_id), json={"status": "pending_review"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending_review"
    assert response.json()["assigned_to_name"] is None


def test_un_autre_gestionnaire_ne_peut_pas_reprendre_un_ticket_pris(
    client, session_factory
):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    first = create_manager_account(client, session_factory, "m1@example.com", "Agent Un")
    second = create_manager_account(client, session_factory, "m2@example.com", "Agent Deux")
    client.patch(status_path(ticket_id), json={"status": "in_progress"}, headers=first)

    response = client.patch(
        status_path(ticket_id), json={"status": "in_progress"}, headers=second
    )
    assert response.status_code == 409


def test_un_autre_gestionnaire_ne_peut_pas_repondre_a_un_ticket_pris(
    client, session_factory
):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    first = create_manager_account(client, session_factory, "m1@example.com", "Agent Un")
    second = create_manager_account(client, session_factory, "m2@example.com", "Agent Deux")
    client.patch(status_path(ticket_id), json={"status": "in_progress"}, headers=first)

    response = client.post(reply_path(ticket_id), json={"reply": "Voici"}, headers=second)
    assert response.status_code == 409


def test_reponse_termine_le_ticket_et_le_client_la_voit(client, session_factory):
    client_id, client_headers = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory)

    response = client.post(
        reply_path(ticket_id), json={"reply": "Voici la solution"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"

    mine = client.get(f"/tickets/{ticket_id}", headers=client_headers).json()
    assert mine["manager_reply"] == "Voici la solution"
    assert mine["status"] == "resolved"


def test_on_ne_peut_pas_repondre_deux_fois(client, session_factory):
    client_id, client_headers = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory)
    client.post(reply_path(ticket_id), json={"reply": "Premiere"}, headers=headers)

    response = client.post(reply_path(ticket_id), json={"reply": "Seconde"}, headers=headers)
    assert response.status_code == 409
    mine = client.get(f"/tickets/{ticket_id}", headers=client_headers).json()
    assert mine["manager_reply"] == "Premiere"


def test_un_ticket_termine_ne_change_plus_de_statut(client, session_factory):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(
        session_factory,
        client_id,
        status=TicketStatus.resolved,
        decision="auto_response",
        ai_answer="ok",
    )
    headers = create_manager_account(client, session_factory)

    response = client.patch(
        status_path(ticket_id), json={"status": "in_progress"}, headers=headers
    )
    assert response.status_code == 409


def test_reponse_vide_est_refusee(client, session_factory):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory)

    response = client.post(reply_path(ticket_id), json={"reply": "   "}, headers=headers)
    assert response.status_code == 422


def test_ticket_inconnu_est_introuvable(client, session_factory):
    headers = create_manager_account(client, session_factory)
    assert client.patch(
        status_path(999), json={"status": "in_progress"}, headers=headers
    ).status_code == 404
    assert client.post(reply_path(999), json={"reply": "x"}, headers=headers).status_code == 404


def test_le_statut_termine_n_est_pas_modifiable_directement(client, session_factory):
    client_id, _ = create_client_account(client)
    ticket_id = add_ticket(session_factory, client_id)
    headers = create_manager_account(client, session_factory)

    response = client.patch(
        status_path(ticket_id), json={"status": "resolved"}, headers=headers
    )
    assert response.status_code == 422