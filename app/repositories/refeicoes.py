from collections.abc import Sequence
from datetime import date, timedelta

from sqlmodel import Session, select

from app.domain.cardapio import inicio_da_semana
from app.models import PratoDB, RefeicaoDB, RefeicaoPratoLink, TipoRefeicao


def criar(
    session: Session, data: date, tipo: TipoRefeicao, pratos: Sequence[PratoDB]
) -> RefeicaoDB:
    refeicao = RefeicaoDB(data=data, tipo=tipo, pratos=list(pratos))
    session.add(refeicao)
    session.commit()
    session.refresh(refeicao)
    return refeicao


def listar_por_data(session: Session, data: date) -> list[RefeicaoDB]:
    consulta = select(RefeicaoDB).where(RefeicaoDB.data == data).order_by(RefeicaoDB.tipo)
    return list(session.exec(consulta))


def listar_da_semana(session: Session, data_ref: date) -> list[RefeicaoDB]:
    """Refeições de segunda a domingo da semana de data_ref, em ordem de data e tipo."""
    segunda = inicio_da_semana(data_ref)
    consulta = (
        select(RefeicaoDB)
        .where(RefeicaoDB.data >= segunda, RefeicaoDB.data < segunda + timedelta(days=7))
        .order_by(RefeicaoDB.data, RefeicaoDB.tipo)
    )
    return list(session.exec(consulta))


def ultima_data_servida(session: Session, prato_id: int, ate: date) -> date | None:
    """Data mais recente, até a data informada, de uma refeição que serviu o prato."""
    consulta = (
        select(RefeicaoDB.data)
        .join(RefeicaoPratoLink)
        .where(RefeicaoPratoLink.prato_id == prato_id, RefeicaoDB.data <= ate)
        .order_by(RefeicaoDB.data.desc())
    )
    return session.exec(consulta).first()
