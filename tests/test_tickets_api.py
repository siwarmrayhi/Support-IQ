"""Tests des routes de tickets (base en mémoire, faux pipeline, aucun LLM)."""

from supportiq.api import routes_tickets
from supportiq.db.models import Role, User
from supportiq.security import hash_password

PASSWORD = "motdepasse123"


def auth_headers(client, email):
    token = client.post(
        "/auth/login", json={"email": email, "password": PASSWORD}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_client_account(client, email="client@example.com"):
    client.post(
        "/auth/signup",
        json={"email": email, "full_name": "Client", "password": PASSWORD},
    )
    return auth_headers(client, email)


def create_manager_account(client, session_factory, email="manager@example.com"):
    with session_factory() as db:
        db.add(
            User(
                email=email,
                full_name="Gestionnaire",
                password_hash=hash_password(PASSWORD),
                role=Role.manager,
            )
        )
        db.commit()
    return auth_headers(client, email)


def post_ticket(client, headers, text):
    return client.post("/tickets", json={"ticket": text}, headers=headers)


def test_creer_un_ticket_sans_jeton_est_refuse(client, fake_pipeline):
    response = client.post("/tickets", json={"ticket": "bonjour"})
    assert response.status_code == 401
    assert fake_pipeline == []


def test_reponse_automatique_donne_un_ticket_termine(client, fake_pipeline):
    headers = create_client_account(client)
    response = post_ticket(client, headers, "question simple")
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "auto_response"
    assert body["status"] == "resolved"
    assert body["ai_answer"] == "Réponse de test"
    assert body["sources"][0]["doc_id"] == "doc_a"


def test_escalade_donne_un_ticket_a_traiter(client, fake_pipeline):
    headers = create_client_account(client)
    body = post_ticket(client, headers, "question hors corpus").json()
    assert body["decision"] == "human_review_required"
    assert body["status"] == "pending_review"
    assert body["ai_answer"] is None
    assert body["sources"] == []


def test_le_texte_du_ticket_est_nettoye_avant_le_pipeline(client, fake_pipeline):
    headers = create_client_account(client)
    body = post_ticket(client, headers, "  question simple  ").json()
    assert body["text"] == "question simple"
    assert fake_pipeline == ["question simple"]


def test_ticket_vide_est_refuse(client, fake_pipeline):
    headers = create_client_account(client)
    assert post_ticket(client, headers, "   ").status_code == 422
    assert fake_pipeline == []


def test_un_gestionnaire_ne_peut_pas_creer_de_ticket(
    client, session_factory, fake_pipeline
):
    headers = create_manager_account(client, session_factory)
    assert post_ticket(client, headers, "question simple").status_code == 403
    assert fake_pipeline == []


class BrokenGraph:
    def invoke(self, state):
        raise RuntimeError("panne simulée")


def test_panne_du_pipeline_envoie_le_ticket_en_revue_humaine(client, monkeypatch):
    monkeypatch.setattr(routes_tickets, "graph", BrokenGraph())
    headers = create_client_account(client)
    response = post_ticket(client, headers, "question simple")
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "pipeline_error"
    assert body["status"] == "pending_review"
    assert body["ai_answer"] is None


def test_historique_ne_liste_que_mes_tickets_du_plus_recent_au_plus_ancien(
    client, fake_pipeline
):
    headers_a = create_client_account(client, "a@example.com")
    headers_b = create_client_account(client, "b@example.com")
    post_ticket(client, headers_a, "premier")
    post_ticket(client, headers_b, "ticket de B")
    post_ticket(client, headers_a, "second")

    response = client.get("/tickets", headers=headers_a)
    assert response.status_code == 200
    assert [t["text"] for t in response.json()] == ["second", "premier"]


def test_je_peux_consulter_mon_ticket(client, fake_pipeline):
    headers = create_client_account(client)
    ticket_id = post_ticket(client, headers, "question simple").json()["id"]
    response = client.get(f"/tickets/{ticket_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["text"] == "question simple"


def test_le_ticket_d_un_autre_client_est_introuvable(client, fake_pipeline):
    headers_a = create_client_account(client, "a@example.com")
    headers_b = create_client_account(client, "b@example.com")
    ticket_id = post_ticket(client, headers_a, "question simple").json()["id"]
    assert client.get(f"/tickets/{ticket_id}", headers=headers_b).status_code == 404


def test_ticket_inexistant_est_introuvable(client, fake_pipeline):
    headers = create_client_account(client)
    assert client.get("/tickets/999", headers=headers).status_code == 404
    