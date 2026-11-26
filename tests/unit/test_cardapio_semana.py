from dataclasses import dataclass
from datetime import date

from app.domain.cardapio import cardapio_da_semana

SEGUNDA = date(2026, 11, 23)
QUARTA = date(2026, 11, 25)
SEXTA = date(2026, 11, 27)
SABADO = date(2026, 11, 28)


@dataclass
class Refeicao:
    data: date
    tipo: str


def test_semana_completa_agrupa_refeicoes_de_segunda_a_sexta():
    refeicoes = [
        Refeicao(date(2026, 11, dia), tipo)
        for dia in range(23, 28)
        for tipo in ("almoco", "jantar")
    ]

    semana = cardapio_da_semana(refeicoes, data_ref=QUARTA)

    assert list(semana) == [date(2026, 11, dia) for dia in range(23, 28)]
    assert all(len(refeicoes_do_dia) == 2 for refeicoes_do_dia in semana.values())


def test_dia_sem_refeicao_aparece_com_lista_vazia():
    almoco_segunda = Refeicao(SEGUNDA, "almoco")

    semana = cardapio_da_semana([almoco_segunda], data_ref=SEXTA)

    assert semana[SEGUNDA] == [almoco_segunda]
    assert semana[QUARTA] == []


def test_refeicoes_do_fim_de_semana_ficam_de_fora():
    almoco_sabado = Refeicao(SABADO, "almoco")

    semana = cardapio_da_semana([almoco_sabado], data_ref=SABADO)

    assert SABADO not in semana
    assert all(refeicoes_do_dia == [] for refeicoes_do_dia in semana.values())
