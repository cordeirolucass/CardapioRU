import re
from datetime import date

from app.domain.avaliacao import Avaliacao
from app.domain.prato import Prato
from app.repositories import avaliacoes, pratos

HOJE = date(2026, 11, 26)


def avaliar(session, prato, *notas):
    for nota in notas:
        avaliacoes.criar(session, prato.id, Avaliacao(nota), criada_em=HOJE)


def celulas(html, testid):
    return re.findall(rf'data-testid="{testid}"[^>]*>([^<]*)<', html)


def test_lista_pratos_em_ordem_com_media_e_total(client, session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    pudim = pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    quibe = pratos.criar(session, Prato("Quibe de abóbora", "vegetariano", 420))
    avaliar(session, feijoada, 3, 4)
    avaliar(session, pudim, 5)
    avaliar(session, quibe, 4, 4, 5)

    resposta = client.get("/ranking")

    assert resposta.status_code == 200
    html = resposta.text
    assert celulas(html, "ranking-prato") == ["Pudim", "Quibe de abóbora", "Feijoada"]
    assert celulas(html, "posicao") == ["1º", "2º", "3º"]
    assert celulas(html, "ranking-media") == ["5,0", "4,3", "3,5"]
    assert celulas(html, "ranking-total") == ["1", "3", "2"]
    assert f'href="/pratos/{quibe.id}"' in html
    assert "Opção vegetariana" in html


def test_empate_na_media_desempata_pelo_numero_de_avaliacoes(client, session):
    arroz = pratos.criar(session, Prato("Arroz", "guarnicao", 200))
    salada = pratos.criar(session, Prato("Salada verde", "salada", 50))
    avaliar(session, arroz, 4)
    avaliar(session, salada, 4, 4)

    html = client.get("/ranking").text

    assert celulas(html, "ranking-prato") == ["Salada verde", "Arroz"]


def test_pratos_sem_avaliacao_ficam_de_fora(client, session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    pratos.criar(session, Prato("Arroz", "guarnicao", 200))
    avaliar(session, feijoada, 4)

    html = client.get("/ranking").text

    assert celulas(html, "ranking-prato") == ["Feijoada"]


def test_sem_avaliacoes_mostra_aviso(client, session):
    pratos.criar(session, Prato("Feijoada", "principal", 750))

    html = client.get("/ranking").text

    assert 'data-testid="ranking-vazio"' in html
    assert 'data-testid="tabela-ranking"' not in html
