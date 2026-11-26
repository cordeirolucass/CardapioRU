from datetime import date

import pytest

from app.domain.avaliacao import Avaliacao
from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import avaliacoes, pratos, refeicoes

SEGUNDA = date(2026, 11, 23)
SEXTA = date(2026, 11, 27)
SEGUNDA_SEGUINTE = date(2026, 11, 30)


@pytest.fixture
def feijoada(session):
    return pratos.criar(session, Prato("Feijoada", "principal", 750))


def test_listar_por_data_traz_almoco_e_jantar_com_seus_pratos(session, feijoada):
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.JANTAR, [feijoada])
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [feijoada])
    refeicoes.criar(session, SEXTA, TipoRefeicao.ALMOCO, [feijoada])

    do_dia = refeicoes.listar_por_data(session, SEGUNDA)

    assert [refeicao.tipo for refeicao in do_dia] == [TipoRefeicao.ALMOCO, TipoRefeicao.JANTAR]
    assert do_dia[0].pratos[0].nome == "Feijoada"


def test_listar_da_semana_ignora_refeicoes_de_outras_semanas(session, feijoada):
    refeicoes.criar(session, SEXTA, TipoRefeicao.ALMOCO, [feijoada])
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [feijoada])
    refeicoes.criar(session, SEGUNDA_SEGUINTE, TipoRefeicao.ALMOCO, [feijoada])

    da_semana = refeicoes.listar_da_semana(session, data_ref=date(2026, 11, 25))

    assert [refeicao.data for refeicao in da_semana] == [SEGUNDA, SEXTA]


def test_listar_avaliacoes_por_prato_traz_so_as_do_prato(session, feijoada):
    pudim = pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    avaliacoes.criar(session, feijoada.id, Avaliacao(5, "Ótima"), criada_em=SEGUNDA)
    avaliacoes.criar(session, pudim.id, Avaliacao(2), criada_em=SEGUNDA)

    da_feijoada = avaliacoes.listar_por_prato(session, feijoada.id)

    assert [(a.nota, a.comentario) for a in da_feijoada] == [(5, "Ótima")]
