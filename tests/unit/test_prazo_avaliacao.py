from datetime import date

from app.domain.avaliacao import pode_avaliar

DATA_REFEICAO = date(2026, 11, 23)


def test_pode_avaliar_no_ultimo_dia_do_prazo():
    assert pode_avaliar(DATA_REFEICAO, hoje=date(2026, 11, 26))


def test_nao_pode_avaliar_depois_do_prazo():
    assert not pode_avaliar(DATA_REFEICAO, hoje=date(2026, 11, 27))
