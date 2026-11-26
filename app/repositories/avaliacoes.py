from datetime import date

from sqlmodel import Session, select

from app.domain.avaliacao import Avaliacao
from app.models import AvaliacaoDB


def criar(session: Session, prato_id: int, avaliacao: Avaliacao, criada_em: date) -> AvaliacaoDB:
    avaliacao_db = AvaliacaoDB(
        prato_id=prato_id,
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        criada_em=criada_em,
    )
    session.add(avaliacao_db)
    session.commit()
    session.refresh(avaliacao_db)
    return avaliacao_db


def listar_por_prato(session: Session, prato_id: int) -> list[AvaliacaoDB]:
    consulta = (
        select(AvaliacaoDB)
        .where(AvaliacaoDB.prato_id == prato_id)
        .order_by(AvaliacaoDB.criada_em.desc(), AvaliacaoDB.id.desc())
    )
    return list(session.exec(consulta))
