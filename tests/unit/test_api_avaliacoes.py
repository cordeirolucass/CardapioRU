from datetime import date

import pytest

from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import avaliacoes, pratos, refeicoes

SEGUNDA = date(2026, 11, 23)


@pytest.fixture
def feijoada(session):
    prato = pratos.criar(session, Prato("Feijoada", "principal", 750))
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [prato])
    return prato


def avaliar(client, prato_id, **corpo):
    return client.post(f"/api/pratos/{prato_id}/avaliacoes", json=corpo)


def test_avaliacao_valida_dentro_do_prazo_e_criada(client, definir_hoje, session, feijoada):
    definir_hoje(date(2026, 11, 25))

    resposta = avaliar(client, feijoada.id, nota=5, comentario="Muito boa")

    assert resposta.status_code == 201
    assert resposta.json()["nota"] == 5
    assert [a.comentario for a in avaliacoes.listar_por_prato(session, feijoada.id)] == [
        "Muito boa"
    ]


def test_avaliar_prato_inexistente_retorna_404(client):
    assert avaliar(client, 999, nota=4).status_code == 404


def test_nota_fora_do_intervalo_retorna_422(client, definir_hoje, feijoada):
    definir_hoje(SEGUNDA)

    resposta = avaliar(client, feijoada.id, nota=6)

    assert resposta.status_code == 422
    assert "entre 1 e 5" in resposta.json()["detail"]


def test_avaliar_depois_do_prazo_retorna_400(client, definir_hoje, feijoada):
    definir_hoje(date(2026, 11, 27))

    assert avaliar(client, feijoada.id, nota=4).status_code == 400
