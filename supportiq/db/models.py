"""Tables de la base : utilisateurs et tickets."""

import enum
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from supportiq.db.database import Base


class Role(str, enum.Enum):
    client = "client"
    manager = "manager"


class TicketStatus(str, enum.Enum):
    pending_review = "pending_review"
    in_progress = "in_progress"
    resolved = "resolved"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.client)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="client", foreign_keys="Ticket.client_id"
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    decision: Mapped[str] = mapped_column(String(30))
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus))
    ai_answer: Mapped[str | None] = mapped_column(Text, default=None)
    sources: Mapped[list] = mapped_column(JSON, default=list)
    manager_reply: Mapped[str | None] = mapped_column(Text, default=None)
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), default=None
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    client: Mapped[User] = relationship(
        back_populates="tickets", foreign_keys=[client_id]
    )