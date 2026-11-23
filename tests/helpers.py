"""Fonctions partagées par les tests d'API."""

from supportiq.db.models import Role, Ticket, TicketStatus, User
from supportiq.security import hash_password

PASSWORD = "motdepasse123"


def auth_headers(client, email):
    token = client.post(
        "/auth/login", json={"email": email, "password": PASSWORD}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_client_account(client, email="client@example.com", name="Client"):
    """Crée un client par l'API. Renvoie (identifiant, en-têtes d'authentification)."""
    response = client.post(
        "/auth/signup",
        json={"email": email, "full_name": name, "password": PASSWORD},
    )
    return response.json()["id"], auth_headers(client, email)


def create_manager_account(
    client, session_factory, email="manager@example.com", name="Gestionnaire"
):
    """Crée un gestionnaire directement dans la base (il ne peut pas s'inscrire)."""
    with session_factory() as db:
        db.add(
            User(
                email=email,
                full_name=name,
                password_hash=hash_password(PASSWORD),
                role=Role.manager,
            )
        )
        db.commit()
    return auth_headers(client, email)


def add_ticket(
    session_factory,
    client_id,
    text="question",
    status=TicketStatus.pending_review,
    decision="human_review_required",
    ai_answer=None,
):
    """Insère un ticket directement dans la base. Renvoie son identifiant."""
    with session_factory() as db:
        ticket = Ticket(
            client_id=client_id,
            text=text,
            decision=decision,
            status=status,
            ai_answer=ai_answer,
            sources=[],
        )
        db.add(ticket)
        db.commit()
        return ticket.id