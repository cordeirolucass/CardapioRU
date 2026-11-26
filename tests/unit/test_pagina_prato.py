from datetime import date

import pytest

from app.domain.avaliacao import Avaliacao
from app.domain.prato import Prato
from app.models import TipoRefeicao
from app.repositories import avaliacoes, pratos, refeicoes

SEGUNDA = date(2026, 11, 23)
QUARTA = date(2026, 11, 25)
SEXTA = date(2026, 11, 27)


@pytest.fixture
def feijoada(session):
    prato = pratos.criar(session, Prato("Feijoada", "principal", 750))
    refeicoes.criar(session, SEGUNDA, TipoRefeicao.ALMOCO, [prato])
    return prato


def avaliar(client, prato_id, **campos):
    return client.post(f"/pratos/{prato_id}/avaliacoes", data=campos, follow_redirects=False)


def test_mostra_dados_do_prato_com_nomes_acentuados(client, session):
    quibe = pratos.criar(session, Prato("Quibe de abóbora", "vegetariano", 420))

    html = client.get(f"/pratos/{quibe.id}").text

    assert "Quibe de abóbora" in html
    assert "Opção vegetariana" in html
    assert "420 kcal" in html


def test_mostra_media_e_lista_de_avaliacoes(client, session, feijoada):
    avaliacoes.criar(session, feijoada.id, Avaliacao(5, "Muito boa"), criada_em=SEGUNDA)
    avaliacoes.criar(session, feijoada.id, Avaliacao(4), criada_em=QUARTA)

    html = client.get(f"/pratos/{feijoada.id}").text

    assert '<strong data-testid="media">4,5</strong>' in html
    assert '<span data-testid="total-avaliacoes">2</span>' in html
    assert html.count('data-testid="avaliacao"') == 2
    assert "Muito boa" in html
    # Mais recente primeiro
    assert html.index("25/11/2026") < html.index("23/11/2026")


def test_prato_sem_avaliacoes_mostra_aviso_e_nenhuma_media(client, feijoada):
    html = client.get(f"/pratos/{feijoada.id}").text

    assert 'data-testid="sem-avaliacoes"' in html
    assert 'data-testid="sem-media"' in html
    assert 'data-testid="media"' not in html


def test_formulario_aparece_dentro_do_prazo(client, definir_hoje, feijoada):
    definir_hoje(QUARTA)

    html = client.get(f"/pratos/{feijoada.id}").text

    assert 'data-testid="form-avaliacao"' in html
    assert f'action="/pratos/{feijoada.id}/avaliacoes"' in html
    assert 'data-testid="prazo-encerrado"' not in html


def test_formulario_some_fora_do_prazo(client, definir_hoje, feijoada):
    definir_hoje(SEXTA)

    html = client.get(f"/pratos/{feijoada.id}").text

    assert 'data-testid="form-avaliacao"' not in html
    assert 'data-testid="prazo-encerrado"' in html


def test_prato_inexistente_retorna_404(client):
    resposta = client.get("/pratos/999")

    assert resposta.status_code == 404
    assert 'data-testid="nao-encontrado"' in resposta.text


def test_enviar_avaliacao_valida_grava_e_redireciona(client, definir_hoje, session, feijoada):
    definir_hoje(QUARTA)

    resposta = avaliar(client, feijoada.id, nota="4", comentario="  Bem temperada  ")

    assert resposta.status_code == 303
    assert resposta.headers["location"] == f"/pratos/{feijoada.id}?avaliado=true"
    [gravada] = avaliacoes.listar_por_prato(session, feijoada.id)
    assert (gravada.nota, gravada.comentario, gravada.criada_em) == (4, "Bem temperada", QUARTA)

    html = client.get(resposta.headers["location"]).text
    assert 'data-testid="avaliacao-enviada"' in html
    assert "Bem temperada" in html


def test_enviar_sem_nota_mostra_erro_e_mantem_comentario(client, definir_hoje, session, feijoada):
    definir_hoje(QUARTA)

    resposta = avaliar(client, feijoada.id, comentario="Esqueci a nota")

    assert resposta.status_code == 422
    assert 'data-testid="erro-avaliacao"' in resposta.text
    assert "Esqueci a nota</textarea>" in resposta.text
    assert avaliacoes.listar_por_prato(session, feijoada.id) == []


def test_enviar_nota_fora_do_intervalo_mostra_erro(client, definir_hoje, session, feijoada):
    definir_hoje(QUARTA)

    resposta = avaliar(client, feijoada.id, nota="6")

    assert resposta.status_code == 422
    assert "entre 1 e 5" in resposta.text
    assert avaliacoes.listar_por_prato(session, feijoada.id) == []


def test_enviar_fora_do_prazo_mostra_erro(client, definir_hoje, session, feijoada):
    definir_hoje(SEXTA)

    resposta = avaliar(client, feijoada.id, nota="5")

    assert resposta.status_code == 400
    assert "3 dias" in resposta.text
    assert avaliacoes.listar_por_prato(session, feijoada.id) == []


def test_enviar_para_prato_inexistente_retorna_404(client):
    assert avaliar(client, 999, nota="5").status_code == 404
