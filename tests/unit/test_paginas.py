"""Testes de fumaça das páginas HTML: cada página responde 200 e mostra o conteúdo principal."""

from datetime import date

import pytest

from app.domain.avaliacao import Avaliacao
from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import avaliacoes, pratos, refeicoes

QUINTA = date(2026, 11, 26)


@pytest.fixture
def cardapio(session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    quibe = pratos.criar(session, Prato("Quibe de abóbora", "vegetariano", 420))
    refeicoes.criar(session, QUINTA, TipoRefeicao.ALMOCO, [feijoada])
    refeicoes.criar(session, QUINTA, TipoRefeicao.JANTAR, [quibe])
    avaliacoes.criar(session, feijoada.id, Avaliacao(5, "Divina"), criada_em=QUINTA)
    avaliacoes.criar(session, feijoada.id, Avaliacao(4), criada_em=QUINTA)
    return {"feijoada": feijoada, "quibe": quibe}


def assert_pagina_html(resposta, titulo):
    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("text/html")
    assert f"<title>{titulo} · CardápioRU</title>" in resposta.text
    for link in ("nav-hoje", "nav-semana", "nav-ranking"):
        assert f'data-testid="{link}"' in resposta.text


def test_pagina_inicial_mostra_almoco_e_jantar_de_hoje(client, definir_hoje, cardapio):
    definir_hoje(QUINTA)

    resposta = client.get("/")

    assert_pagina_html(resposta, "Cardápio de hoje")
    html = resposta.text
    assert "Quinta, 26/11/2026" in html
    assert 'data-testid="refeicao-almoco"' in html
    assert 'data-testid="refeicao-jantar"' in html
    assert "Feijoada" in html
    assert "Quibe de abóbora" in html
    assert 'data-testid="sem-cardapio"' not in html


def test_pagina_da_semana_mostra_os_cinco_dias_e_o_filtro(client, definir_hoje, cardapio):
    definir_hoje(QUINTA)

    resposta = client.get("/semana")

    assert_pagina_html(resposta, "Cardápio da semana")
    html = resposta.text
    assert 'data-testid="form-filtro"' in html
    assert [d for d in range(23, 28) if f'data-testid="dia-2026-11-{d}"' in html] == [
        23,
        24,
        25,
        26,
        27,
    ]
    assert html.count('data-testid="prato"') == 2
    assert html.count('data-testid="sem-cardapio"') == 4


def test_pagina_do_prato_mostra_media_avaliacoes_e_formulario(client, definir_hoje, cardapio):
    definir_hoje(QUINTA)

    resposta = client.get(f"/pratos/{cardapio['feijoada'].id}")

    assert_pagina_html(resposta, "Feijoada")
    html = resposta.text
    assert '<strong data-testid="media">4,5</strong>' in html
    assert html.count('data-testid="avaliacao"') == 2
    assert "Divina" in html
    assert 'data-testid="form-avaliacao"' in html


def test_pagina_de_ranking_lista_o_prato_avaliado(client, cardapio):
    resposta = client.get("/ranking")

    assert_pagina_html(resposta, "Ranking dos pratos")
    html = resposta.text
    assert html.count('data-testid="item-ranking"') == 1
    assert f'href="/pratos/{cardapio["feijoada"].id}" data-testid="ranking-prato">Feijoada' in html
    assert '<td data-testid="ranking-media">4,5</td>' in html
    assert '<td data-testid="ranking-total">2</td>' in html
