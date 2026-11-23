"""Client HTTP de l'API SupportIQ."""

import os

import httpx

API_URL = os.getenv("SUPPORTIQ_API_URL", "http://127.0.0.1:8000")
TIMEOUT = 120.0


class ApiError(Exception):
    """Erreur lisible renvoyée par l'API."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _message(response: httpx.Response) -> str:
    try:
        detail = response.json().get("detail")
    except ValueError:
        detail = None
    if isinstance(detail, str):
        return detail
    if response.status_code == 422:
        return "Les informations saisies sont invalides."
    return f"Erreur {response.status_code}"


def _request(method: str, path: str, token: str | None = None, **kwargs):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = httpx.request(
            method, f"{API_URL}{path}", headers=headers, timeout=TIMEOUT, **kwargs
        )
    except httpx.HTTPError as exc:
        raise ApiError(
            "Le serveur est injoignable. Vérifiez que l'API est lancée."
        ) from exc
    if response.status_code >= 400:
        raise ApiError(_message(response), response.status_code)
    return response.json()


def signup(email: str, full_name: str, password: str) -> dict:
    return _request(
        "POST",
        "/auth/signup",
        json={"email": email, "full_name": full_name, "password": password},
    )


def login(email: str, password: str) -> dict:
    return _request("POST", "/auth/login", json={"email": email, "password": password})


def list_tickets(token: str) -> list[dict]:
    return _request("GET", "/tickets", token=token)


def create_ticket(token: str, text: str) -> dict:
    return _request("POST", "/tickets", token=token, json={"ticket": text})