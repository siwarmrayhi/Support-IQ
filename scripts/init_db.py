"""Crée les tables de la base SupportIQ."""

from sqlalchemy import inspect

from supportiq.config import settings
from supportiq.db import models  # noqa: F401 (enregistre les tables)
from supportiq.db.database import Base, engine

settings.database_path.parent.mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(engine)

inspector = inspect(engine)
for table in inspector.get_table_names():
    columns = [c["name"] for c in inspector.get_columns(table)]
    print(f"{table}: {columns}")