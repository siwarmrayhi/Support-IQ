"""API SupportIQ : point d'entrée HTTP."""

from fastapi import FastAPI
from supportiq.api.routes_manager import router as manager_router

from supportiq.api.routes_auth import router as auth_router
from supportiq.api.routes_tickets import router as tickets_router

app = FastAPI(title="SupportIQ")
app.include_router(auth_router)
app.include_router(tickets_router)
app.include_router(manager_router)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}