"""Préparation commune des tests : base en mémoire, client HTTP, faux pipeline."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from supportiq.api import routes_tickets
from supportiq.api.deps import get_db
from supportiq.api.routes_auth import router as auth_router
from supportiq.api.routes_tickets import router as tickets_router
from supportiq.db import models  # noqa: F401 (enregistre les tables)
from supportiq.db.database import Base


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(tickets_router)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def fake_pipeline(monkeypatch):
    """Remplace l'IA : répond tout de suite, sans aucun appel LLM."""
    calls = []

    def fake(text):
        calls.append(text)
        if "hors corpus" in text:
            return {"status": "human_review_required", "answer": None, "sources": []}
        return {
            "status": "auto_response",
            "answer": "Réponse de test",
            "sources": [{"doc_id": "doc_a", "title": "Doc A", "source_type": "faq"}],
        }

    monkeypatch.setattr(routes_tickets, "run_pipeline", fake)
    return calls