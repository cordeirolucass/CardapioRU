import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cardapioru.db")


def criar_engine(url: str = DATABASE_URL):
    """Cria a engine do banco. No SQLite, permite o uso da conexão em outras threads."""
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


engine = criar_engine()


def criar_tabelas() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Dependência do FastAPI que abre uma sessão por requisição."""
    with Session(engine) as session:
        yield session
