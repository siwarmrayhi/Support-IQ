"""Routes du gestionnaire : liste complète, prise en charge et réponse."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from supportiq.api.deps import get_db, require_manager
from supportiq.api.schemas import (
    ManagerTicketOut,
    ReplyRequest,
    StatusChangeRequest,
    TicketOut,
)
from supportiq.db.models import Ticket, TicketStatus, User

router = APIRouter(prefix="/manager", tags=["manager"])


def to_manager_out(ticket: Ticket) -> ManagerTicketOut:
    """Fiche du ticket enrichie du nom du client et du gestionnaire."""
    data = TicketOut.model_validate(ticket).model_dump()
    return ManagerTicketOut(
        **data,
        client_name=ticket.client.full_name,
        client_email=ticket.client.email,
        assigned_to_id=ticket.assigned_to_id,
        assigned_to_name=ticket.assigned_to.full_name if ticket.assigned_to else None,
        
    )


def load_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(404, "Ticket introuvable")
    return ticket


def ensure_available(ticket: Ticket, manager: User) -> None:
    """Un ticket terminé ne change plus ; un ticket pris appartient à son gestionnaire."""
    if ticket.status == TicketStatus.resolved:
        raise HTTPException(409, "Ce ticket est déjà terminé")
    if ticket.assigned_to_id not in (None, manager.id):
        raise HTTPException(
            409, "Ce ticket est pris en charge par un autre gestionnaire"
        )


@router.get("/tickets", response_model=list[ManagerTicketOut])
def list_all_tickets(
    status_filter: TicketStatus | None = Query(default=None, alias="status"),
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> list[ManagerTicketOut]:
    query = (
        select(Ticket)
        .options(selectinload(Ticket.client), selectinload(Ticket.assigned_to))
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
    )
    if status_filter is not None:
        query = query.where(Ticket.status == status_filter)
    return [to_manager_out(ticket) for ticket in db.scalars(query)]


@router.patch("/tickets/{ticket_id}/status", response_model=ManagerTicketOut)
def change_status(
    ticket_id: int,
    data: StatusChangeRequest,
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> ManagerTicketOut:
    ticket = load_ticket(db, ticket_id)
    ensure_available(ticket, manager)
    new_status = TicketStatus(data.status)
    if new_status == ticket.status:
        raise HTTPException(409, "Le ticket a déjà ce statut")

    ticket.status = new_status
    ticket.assigned_to_id = manager.id if new_status == TicketStatus.in_progress else None
    db.commit()
    db.refresh(ticket)
    return to_manager_out(ticket)


@router.post("/tickets/{ticket_id}/reply", response_model=ManagerTicketOut)
def reply_to_ticket(
    ticket_id: int,
    data: ReplyRequest,
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> ManagerTicketOut:
    ticket = load_ticket(db, ticket_id)
    ensure_available(ticket, manager)

    ticket.manager_reply = data.reply
    ticket.status = TicketStatus.resolved
    ticket.assigned_to_id = manager.id
    db.commit()
    db.refresh(ticket)
    return to_manager_out(ticket)