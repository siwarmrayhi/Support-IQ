"""Tests des mots de passe et des jetons (aucun appel LLM, aucune base)."""

import jwt
import pytest

from supportiq.config import settings
from supportiq.security import (
    ALGORITHM,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_le_hash_n_est_pas_le_mot_de_passe():
    assert hash_password("secret123") != "secret123"


def test_bon_mot_de_passe_accepte():
    assert verify_password("secret123", hash_password("secret123"))


def test_mauvais_mot_de_passe_refuse():
    assert not verify_password("autre", hash_password("secret123"))


def test_meme_mot_de_passe_donne_deux_hash_differents():
    assert hash_password("secret123") != hash_password("secret123")


def test_token_contient_identifiant_et_role():
    payload = decode_access_token(create_access_token(7, "client"))
    assert payload["sub"] == "7"
    assert payload["role"] == "client"


def test_token_modifie_est_refuse():
    assert decode_access_token(create_access_token(7, "client") + "x") is None


def test_token_expire_est_refuse():
    expired = jwt.encode(
        {"sub": "7", "role": "client", "exp": 1},
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )
    assert decode_access_token(expired) is None


def test_mot_de_passe_trop_long_leve_une_erreur():
    with pytest.raises(ValueError):
        hash_password("a" * 100)