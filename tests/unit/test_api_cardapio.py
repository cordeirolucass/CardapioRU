from datetime import date

import pytest

from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import pratos, refeicoes

SEGUNDA = date(2026, 11, 23)
QUINTA = date(2026, 11, 26)


@pytest.fixture(autouse=True)
def cardapio(session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    pudim = pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    refeicoes.criar(session, QUINTA, TipoRefeicao.ALMOCO, [feijoada, pudim])
    refeicoes.criar(session, QUINTA, TipoRefeicao.JANTAR, [feijoada])
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [pudim])


def test_cardapio_de_hoje_traz_almoco_e_jantar_com_os_pratos(client, definir_hoje):
    definir_hoje(QUINTA)

    corpo = client.get("/api/cardapio/hoje").json()

    assert corpo["data"] == "2026-11-26"
    assert [r["tipo"] for r in corpo["refeicoes"]] == ["almoco", "jantar"]
    assert [p["nome"] for p in corpo["refeicoes"][0]["pratos"]] == ["Feijoada", "Pudim"]


def test_dia_sem_cardapio_retorna_lista_de_refeicoes_vazia(client, definir_hoje):
    definir_hoje(date(2026, 11, 25))

    resposta = client.get("/api/cardapio/hoje")

    assert resposta.status_code == 200
    assert resposta.json()["refeicoes"] == []


def test_cardapio_da_semana_lista_os_cinco_dias_uteis(client, definir_hoje):
    definir_hoje(QUINTA)

    dias = client.get("/api/cardapio/semana").json()["dias"]

    assert [dia["data"] for dia in dias] == [f"2026-11-{d}" for d in range(23, 28)]
    assert [len(dia["refeicoes"]) for dia in dias] == [1, 0, 0, 2, 0]
