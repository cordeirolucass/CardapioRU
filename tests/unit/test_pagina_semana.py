import re
from datetime import date

import pytest

from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import pratos, refeicoes

SEGUNDA = date(2026, 11, 23)
QUINTA = date(2026, 11, 26)
SABADO = date(2026, 11, 28)


@pytest.fixture(autouse=True)
def cardapio(session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    quibe = pratos.criar(session, Prato("Quibe de abóbora", "vegetariano", 420))
    pudim = pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    refeicoes.criar(session, QUINTA, TipoRefeicao.ALMOCO, [feijoada, pudim])
    refeicoes.criar(session, QUINTA, TipoRefeicao.JANTAR, [quibe])
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [pudim])
    refeicoes.criar(session, SABADO, TipoRefeicao.ALMOCO, [feijoada])


def test_pagina_da_semana_mostra_uma_tabela_por_dia_util(client, definir_hoje):
    definir_hoje(QUINTA)

    resposta = client.get("/semana")

    assert resposta.status_code == 200
    html = resposta.text
    for dia in range(23, 28):
        assert f'data-testid="dia-2026-11-{dia}"' in html
    assert 'data-testid="dia-2026-11-28"' not in html
    assert html.count("<table") == 2
    assert "Segunda, 23/11/2026" in html
    assert "Sexta, 27/11/2026" in html


def test_pagina_da_semana_mostra_pratos_com_nomes_acentuados(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana").text

    assert html.count('data-testid="prato"') == 4
    assert "Almoço" in html
    assert "Jantar" in html
    assert "Opção vegetariana" in html
    assert "Quibe de abóbora" in html


def test_dias_sem_cardapio_aparecem_com_aviso(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana").text

    assert html.count('data-testid="sem-cardapio"') == 3


def test_destaca_o_dia_de_hoje(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana").text

    assert html.count('data-testid="dia-hoje"') == 1
    secao_quinta = html.split('data-testid="dia-2026-11-26"')[1].split("</section>")[0]
    assert 'data-testid="dia-hoje"' in secao_quinta


def test_no_fim_de_semana_mostra_a_semana_corrente_sem_destaque(client, definir_hoje):
    definir_hoje(SABADO)

    html = client.get("/semana").text

    assert 'data-testid="dia-2026-11-23"' in html
    assert 'data-testid="dia-hoje"' not in html


def pratos_da_pagina(html):
    return re.findall(r'data-testid="prato".*?<a href="/pratos/\d+">([^<]*)</a>', html, re.S)


def test_formulario_de_filtro_aparece_na_pagina(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana").text

    assert 'data-testid="form-filtro"' in html
    assert 'data-testid="filtro-vegetariano"' in html
    assert html.count("<option") == 6  # "Todas" + 5 categorias
    assert "Guarnição" in html
    assert 'data-testid="limpar-filtro"' not in html


def test_filtra_por_categoria(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana", params={"categoria": "sobremesa"}).text

    assert pratos_da_pagina(html) == ["Pudim", "Pudim"]
    assert '<option value="sobremesa" selected>' in html
    assert 'data-testid="limpar-filtro"' in html


def test_filtra_so_vegetarianos(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana", params={"vegetariano": "true"}).text

    assert pratos_da_pagina(html) == ["Quibe de abóbora"]
    assert 'data-testid="refeicao-almoco"' not in html
    assert "checked" in html


def test_dia_com_cardapio_sem_prato_no_filtro_mostra_aviso_proprio(client, definir_hoje):
    definir_hoje(QUINTA)

    html = client.get("/semana", params={"vegetariano": "true"}).text

    secao_segunda = html.split('data-testid="dia-2026-11-23"')[1].split("</section>")[0]
    assert 'data-testid="sem-resultado"' in secao_segunda
    assert html.count('data-testid="sem-cardapio"') == 3


def test_categoria_desconhecida_e_ignorada(client, definir_hoje):
    definir_hoje(QUINTA)

    resposta = client.get("/semana", params={"categoria": "pizza"})

    assert resposta.status_code == 200
    assert len(pratos_da_pagina(resposta.text)) == 4
