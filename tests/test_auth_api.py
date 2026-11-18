"""Tests des routes d'authentification (base en mémoire, aucun LLM)."""

SIGNUP = {
    "email": "client@example.com",
    "full_name": "Client Test",
    "password": "motdepasse123",
}


def signup(client, **overrides):
    return client.post("/auth/signup", json={**SIGNUP, **overrides})


def login(client, email="client@example.com", password="motdepasse123"):
    return client.post("/auth/login", json={"email": email, "password": password})


def test_signup_cree_un_client_sans_exposer_le_mot_de_passe(client):
    response = signup(client)
    assert response.status_code == 201
    body = response.json()
    assert body["role"] == "client"
    assert "password" not in body
    assert "password_hash" not in body


def test_signup_ne_permet_pas_de_choisir_le_role(client):
    response = signup(client, role="manager")
    assert response.status_code == 201
    assert response.json()["role"] == "client"


def test_signup_email_deja_utilise_est_refuse(client):
    signup(client)
    assert signup(client).status_code == 409


def test_signup_ignore_la_casse_de_l_email(client):
    signup(client)
    assert signup(client, email="CLIENT@Example.com").status_code == 409


def test_signup_mot_de_passe_trop_court_est_refuse(client):
    assert signup(client, password="court").status_code == 422


def test_login_bon_mot_de_passe_renvoie_un_jeton(client):
    signup(client)
    response = login(client)
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_mauvais_mot_de_passe_est_refuse(client):
    signup(client)
    assert login(client, password="mauvais-mot-de-passe").status_code == 401


def test_login_email_inconnu_donne_le_meme_message(client):
    signup(client)
    mauvais_mot_de_passe = login(client, password="mauvais-mot-de-passe")
    email_inconnu = login(client, email="inconnu@example.com")
    assert email_inconnu.status_code == 401
    assert email_inconnu.json() == mauvais_mot_de_passe.json()


def test_me_sans_jeton_est_refuse(client):
    assert client.get("/auth/me").status_code == 401


def test_me_avec_jeton_renvoie_le_profil(client):
    signup(client)
    token = login(client).json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "client@example.com"


def test_me_avec_jeton_modifie_est_refuse(client):
    signup(client)
    token = login(client).json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}x"})
    assert response.status_code == 401