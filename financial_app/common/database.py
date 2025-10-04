from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from .settings import Settings

engine = create_engine(Settings().DATABASE_URL)

tables_registry = registry()


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
