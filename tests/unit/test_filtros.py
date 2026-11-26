import pytest

from app.domain.filtros import filtrar_pratos
from app.domain.prato import Prato


@pytest.fixture
def pratos():
    return [
        Prato(nome="Feijoada", categoria="principal", calorias=650),
        Prato(nome="Strogonoff de grão-de-bico", categoria="vegetariano", calorias=480),
        Prato(nome="Salada verde", categoria="salada", calorias=40, vegetariano=True),
        Prato(nome="Salpicão", categoria="salada", calorias=300),
    ]


def nomes(pratos):
    return [prato.nome for prato in pratos]


def test_sem_filtros_retorna_todos_os_pratos(pratos):
    assert filtrar_pratos(pratos) == pratos


def test_filtro_por_categoria_retorna_so_pratos_da_categoria(pratos):
    resultado = filtrar_pratos(pratos, categoria="salada")

    assert nomes(resultado) == ["Salada verde", "Salpicão"]


def test_filtro_vegetariano_retorna_so_pratos_vegetarianos(pratos):
    resultado = filtrar_pratos(pratos, apenas_vegetarianos=True)

    assert nomes(resultado) == ["Strogonoff de grão-de-bico", "Salada verde"]


def test_filtros_combinados_exigem_as_duas_condicoes(pratos):
    resultado = filtrar_pratos(pratos, categoria="salada", apenas_vegetarianos=True)

    assert nomes(resultado) == ["Salada verde"]
