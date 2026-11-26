from datetime import date

from sqlmodel import func, select

from app.models import AvaliacaoDB, PratoDB, RefeicaoDB
from app.seed import popular_banco

HOJE = date(2026, 11, 26)


def contar(session, modelo):
    return session.exec(select(func.count()).select_from(modelo)).one()


def test_rodar_o_seed_duas_vezes_nao_duplica_os_dados(session):
    assert popular_banco(session, HOJE) is True
    totais = [contar(session, modelo) for modelo in (PratoDB, RefeicaoDB, AvaliacaoDB)]

    assert popular_banco(session, HOJE) is False
    assert [contar(session, modelo) for modelo in (PratoDB, RefeicaoDB, AvaliacaoDB)] == totais
    assert totais[1] == 10  # almoço e jantar de segunda a sexta
