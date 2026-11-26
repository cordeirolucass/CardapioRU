"""Testa a subida real do app: criação das tabelas, seed e sessão por requisição.

Os outros testes trocam o banco por um em memória (fixture client). Aqui o app usa a engine
de app.database, apontada para um SQLite temporário, como acontece em produção.
"""

import pytest
from fastapi.testclient import TestClient

import app.database
import app.main
from app.database import criar_engine
from app.main import app as aplicacao
from app.seed import PRATOS


@pytest.fixture
def banco_temporario(tmp_path, monkeypatch):
    engine = criar_engine(f"sqlite:///{(tmp_path / 'teste.db').as_posix()}")
    monkeypatch.setattr(app.database, "engine", engine)
    monkeypatch.setattr(app.main, "engine", engine)
    yield
    engine.dispose()


def test_subida_cria_tabelas_e_popula_banco_vazio(banco_temporario):
    with TestClient(aplicacao) as client:
        pratos = client.get("/api/pratos").json()
        dias = client.get("/api/cardapio/semana").json()["dias"]

    assert len(pratos) == len(PRATOS)
    assert all(len(dia["refeicoes"]) == 2 for dia in dias)


def test_subir_de_novo_nao_duplica_o_cardapio(banco_temporario):
    with TestClient(aplicacao):
        pass

    with TestClient(aplicacao) as client:
        pratos = client.get("/api/pratos").json()
        ranking = client.get("/api/ranking").json()

    assert len(pratos) == len(PRATOS)
    assert sum(item["total_avaliacoes"] for item in ranking) == 5


def test_avaliacao_gravada_numa_subida_continua_na_proxima(banco_temporario):
    # Arroz branco é servido todo dia útil no seed, então está sempre no prazo para avaliar.
    with TestClient(aplicacao) as client:
        arroz = next(p for p in client.get("/api/pratos").json() if p["nome"] == "Arroz branco")
        resposta = client.post(f"/api/pratos/{arroz['id']}/avaliacoes", json={"nota": 5})

    with TestClient(aplicacao) as client:
        ranking = client.get("/api/ranking").json()

    assert resposta.status_code == 201
    assert any(item["prato"]["nome"] == "Arroz branco" for item in ranking)
