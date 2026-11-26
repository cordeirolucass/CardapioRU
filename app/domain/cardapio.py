from collections.abc import Iterable
from datetime import date, timedelta
from typing import Protocol

DIAS_UTEIS = 5


class TemData(Protocol):
    data: date


def inicio_da_semana(data_ref: date) -> date:
    """Segunda-feira da semana de data_ref."""
    return data_ref - timedelta(days=data_ref.weekday())


def dias_uteis_da_semana(data_ref: date) -> list[date]:
    """Datas de segunda a sexta da semana de data_ref."""
    segunda = inicio_da_semana(data_ref)
    return [segunda + timedelta(days=i) for i in range(DIAS_UTEIS)]


def cardapio_da_semana[R: TemData](refeicoes: Iterable[R], data_ref: date) -> dict[date, list[R]]:
    """Agrupa as refeições da semana de data_ref por dia útil, de segunda a sexta.

    Todo dia útil aparece no resultado, mesmo sem refeições. Refeições de outras
    semanas ou do fim de semana ficam de fora.
    """
    semana: dict[date, list[R]] = {dia: [] for dia in dias_uteis_da_semana(data_ref)}
    for refeicao in refeicoes:
        if refeicao.data in semana:
            semana[refeicao.data].append(refeicao)
    return semana
