"""API SupportIQ : point d'entrée HTTP du pipeline."""

from fastapi import FastAPI

from supportiq.api.schemas import TicketRequest, TicketResponse
from supportiq.graph.workflow import graph
from supportiq.api.routes_auth import router as auth_router

app = FastAPI(title="SupportIQ")

app.include_router(auth_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(request: TicketRequest) -> TicketResponse:
    result = graph.invoke({"ticket": request.ticket, "generation_attempts": 0})
    return TicketResponse(
        status=result["status"],
        answer=result["answer"],
        sources=result["sources"],
    )