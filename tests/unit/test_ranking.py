from app.domain.avaliacao import Avaliacao
from app.domain.estatisticas import ranking_pratos


def notas(*valores):
    return [Avaliacao(nota=valor) for valor in valores]


def nomes_no_ranking(ranking):
    return [item.prato for item in ranking]


def test_ranking_ordena_pela_maior_media():
    ranking = ranking_pratos(
        [
            ("Arroz", notas(3)),
            ("Feijoada", notas(5)),
            ("Pudim", notas(4)),
        ]
    )

    assert nomes_no_ranking(ranking) == ["Feijoada", "Pudim", "Arroz"]


def test_ranking_desempata_pelo_numero_de_avaliacoes():
    ranking = ranking_pratos(
        [
            ("Feijoada", notas(4, 5)),
            ("Pudim", notas(5, 4, 5, 4)),
        ]
    )

    assert nomes_no_ranking(ranking) == ["Pudim", "Feijoada"]


def test_ranking_ignora_pratos_sem_avaliacao():
    ranking = ranking_pratos(
        [
            ("Salada", []),
            ("Pudim", notas(5)),
        ]
    )

    assert nomes_no_ranking(ranking) == ["Pudim"]


def test_ranking_informa_media_e_total_de_avaliacoes():
    [item] = ranking_pratos([("Feijoada", notas(5, 4, 4))])

    assert item.media == 4.3
    assert item.total_avaliacoes == 3


def test_ranking_sem_pratos_e_vazio():
    assert ranking_pratos([]) == []
