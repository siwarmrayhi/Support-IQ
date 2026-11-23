"""Crée un compte gestionnaire (un gestionnaire ne peut pas s'inscrire lui-même)."""

import argparse
import getpass
import sys

from sqlalchemy import select

from supportiq.db import models  # noqa: F401 (enregistre les tables)
from supportiq.db.database import Base, SessionLocal, engine
from supportiq.db.models import Role, User
from supportiq.security import hash_password

MIN_LENGTH = 8


def main() -> None:
    parser = argparse.ArgumentParser(description="Crée un compte gestionnaire.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    email = args.email.strip().lower()
    name = args.name.strip()
    if "@" not in email or not name:
        sys.exit("Adresse e-mail ou nom invalide.")

    password = getpass.getpass("Mot de passe : ")
    if len(password) < MIN_LENGTH:
        sys.exit(f"Le mot de passe doit contenir au moins {MIN_LENGTH} caractères.")
    if getpass.getpass("Confirmez le mot de passe : ") != password:
        sys.exit("Les mots de passe ne correspondent pas.")
    try:
        password_hash = hash_password(password)
    except ValueError as exc:
        sys.exit(str(exc))

    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.scalar(select(User).where(User.email == email)):
            sys.exit(f"Un compte existe déjà pour {email}.")
        db.add(
            User(
                email=email,
                full_name=name,
                password_hash=password_hash,
                role=Role.manager,
            )
        )
        db.commit()
    print(f"Compte gestionnaire créé : {email}")


if __name__ == "__main__":
    main()