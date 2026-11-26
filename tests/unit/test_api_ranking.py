from datetime import date

from app.domain.avaliacao import Avaliacao
from app.domain.prato import Prato
from app.repositories import avaliacoes, pratos

HOJE = date(2026, 11, 26)


def avaliar(session, prato, *notas):
    for nota in notas:
        avaliacoes.criar(session, prato.id, Avaliacao(nota), criada_em=HOJE)


def test_ranking_ordena_pela_media_e_ignora_pratos_sem_avaliacao(client, session):
    feijoada = pratos.criar(session, Prato("Feijoada", "principal", 750))
    pudim = pratos.criar(session, Prato("Pudim", "sobremesa", 300))
    pratos.criar(session, Prato("Arroz", "guarnicao", 200))
    avaliar(session, feijoada, 3, 4)
    avaliar(session, pudim, 5)

    ranking = client.get("/api/ranking").json()

    assert [(i["posicao"], i["prato"]["nome"], i["media"]) for i in ranking] == [
        (1, "Pudim", 5.0),
        (2, "Feijoada", 3.5),
    ]
    assert ranking[1]["total_avaliacoes"] == 2


def test_ranking_sem_avaliacoes_retorna_lista_vazia(client, session):
    pratos.criar(session, Prato("Feijoada", "principal", 750))

    assert client.get("/api/ranking").json() == []
