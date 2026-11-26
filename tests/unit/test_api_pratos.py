import pytest

from app.domain.prato import Prato
from app.repositories import pratos


@pytest.fixture(autouse=True)
def cardapio(session):
    pratos.criar(session, Prato("Feijoada", "principal", 750))
    pratos.criar(session, Prato("Lentilha com legumes", "vegetariano", 390))
    pratos.criar(session, Prato("Salada verde", "salada", 40, vegetariano=True))


def nomes(resposta):
    return [prato["nome"] for prato in resposta.json()]


def test_lista_todos_os_pratos_sem_filtro(client):
    resposta = client.get("/api/pratos")

    assert resposta.status_code == 200
    assert nomes(resposta) == ["Feijoada", "Lentilha com legumes", "Salada verde"]


def test_filtra_por_categoria_e_apenas_vegetarianos(client):
    assert nomes(client.get("/api/pratos", params={"categoria": "salada"})) == ["Salada verde"]
    assert nomes(client.get("/api/pratos", params={"vegetariano": True})) == [
        "Lentilha com legumes",
        "Salada verde",
    ]


def test_categoria_invalida_retorna_422(client):
    assert client.get("/api/pratos", params={"categoria": "lanche"}).status_code == 422
