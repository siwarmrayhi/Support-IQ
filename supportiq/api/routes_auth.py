"""Routes d'authentification : inscription et connexion."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from supportiq.api.deps import get_current_user, get_db
from supportiq.api.schemas import LoginRequest, SignupRequest, TokenResponse, UserOut
from supportiq.db.models import Role, User
from supportiq.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Empreinte factice : un e-mail inconnu prend le même temps qu'un mauvais
# mot de passe, pour ne rien révéler sur les comptes existants.
_DUMMY_HASH = hash_password("mot-de-passe-factice")


def _normalize(email: str) -> str:
    return email.strip().lower()


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)) -> User:
    email = _normalize(data.email)
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Cette adresse e-mail est déjà utilisée"
        )
    try:
        password_hash = hash_password(data.password)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))

    user = User(
        email=email,
        full_name=data.full_name.strip(),
        password_hash=password_hash,
        role=Role.client,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Cette adresse e-mail est déjà utilisée"
        )
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == _normalize(data.email)))
    password_hash = user.password_hash if user else _DUMMY_HASH
    valid = verify_password(data.password, password_hash)
    if user is None or not valid:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.id, user.role.value)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> User:
    return user