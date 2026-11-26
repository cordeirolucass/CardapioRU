from app.domain.prato import Prato
from app.repositories import pratos


def test_criar_prato_atribui_id_e_guarda_os_dados(session):
    criado = pratos.criar(session, Prato("Feijoada", "principal", 750))

    assert criado.id is not None
    assert (criado.nome, criado.categoria, criado.calorias) == ("Feijoada", "principal", 750)


def test_listar_retorna_pratos_em_ordem_alfabetica(session):
    pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    pratos.criar(session, Prato("Arroz", "guarnicao", 200))

    nomes = [prato.nome for prato in pratos.listar(session)]

    assert nomes == ["Arroz", "Pudim"]


def test_buscar_por_id_inexistente_retorna_none(session):
    assert pratos.buscar_por_id(session, 999) is None
