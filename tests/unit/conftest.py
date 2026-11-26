import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.models  # noqa: F401  (registra as tabelas no metadata)
from app.database import get_session
from app.dependencies import hoje
from app.main import app


@pytest.fixture
def session():
    """Sessão com um banco SQLite em memória, novo a cada teste."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(session):
    """TestClient da API usando o banco em memória no lugar do banco real."""
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def definir_hoje(client):
    """Fixa a data de "hoje" vista pela API."""

    def definir(data):
        app.dependency_overrides[hoje] = lambda: data

    return definir
