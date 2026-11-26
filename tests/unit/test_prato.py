import pytest

from app.domain.prato import Categoria, Prato


def test_prato_valido_remove_espacos_do_nome_e_converte_categoria():
    prato = Prato(nome="  Feijoada  ", categoria="principal", calorias=650)

    assert prato.nome == "Feijoada"
    assert prato.categoria == Categoria.PRINCIPAL
    assert prato.calorias == 650


@pytest.mark.parametrize("nome", ["", "   "])
def test_prato_com_nome_vazio_e_rejeitado(nome):
    with pytest.raises(ValueError, match="nome"):
        Prato(nome=nome, categoria=Categoria.PRINCIPAL, calorias=500)


def test_prato_com_categoria_inexistente_e_rejeitado():
    with pytest.raises(ValueError, match="Categoria inválida"):
        Prato(nome="Coxinha", categoria="lanche", calorias=300)


def test_prato_com_calorias_negativas_e_rejeitado():
    with pytest.raises(ValueError, match="calorias"):
        Prato(nome="Arroz", categoria=Categoria.GUARNICAO, calorias=-1)


def test_prato_da_categoria_vegetariano_e_vegetariano():
    prato = Prato(nome="Strogonoff de grão-de-bico", categoria="vegetariano", calorias=480)

    assert prato.e_vegetariano


def test_prato_de_outra_categoria_so_e_vegetariano_se_marcado():
    salada = Prato(nome="Salada verde", categoria="salada", calorias=40, vegetariano=True)
    frango = Prato(nome="Frango assado", categoria="principal", calorias=550)

    assert salada.e_vegetariano
    assert not frango.e_vegetariano
