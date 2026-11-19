"""Routes des tickets : création (avec pipeline IA) et historique du client."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from supportiq.api.deps import get_db, require_client
from supportiq.api.schemas import TicketOut, TicketRequest
from supportiq.db.models import Ticket, TicketStatus, User
from supportiq.graph.workflow import graph

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["tickets"])


def status_from_decision(decision: str) -> TicketStatus:
    """Réponse automatique : terminé. Sinon : à traiter par un humain."""
    if decision == "auto_response":
        return TicketStatus.resolved
    return TicketStatus.pending_review


def run_pipeline(text: str) -> dict:
    """Lance le pipeline IA. En cas de panne, le ticket part chez un humain."""
    try:
        return graph.invoke({"ticket": text, "generation_attempts": 0})
    except Exception:
        logger.exception("Pipeline en échec : ticket envoyé en revue humaine")
        return {"status": "pipeline_error", "answer": None, "sources": []}


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    request: TicketRequest,
    user: User = Depends(require_client),
    db: Session = Depends(get_db),
) -> Ticket:
    result = run_pipeline(request.ticket)
    ticket = Ticket(
        client_id=user.id,
        text=request.ticket,
        decision=result["status"],
        status=status_from_decision(result["status"]),
        ai_answer=result["answer"],
        sources=result["sources"],
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketOut])
def list_my_tickets(
    user: User = Depends(require_client),
    db: Session = Depends(get_db),
) -> list[Ticket]:
    query = (
        select(Ticket)
        .where(Ticket.client_id == user.id)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
    )
    return list(db.scalars(query))


@router.get("/{ticket_id}", response_model=TicketOut)
def get_my_ticket(
    ticket_id: int,
    user: User = Depends(require_client),
    db: Session = Depends(get_db),
) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None or ticket.client_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket introuvable")
    return ticket