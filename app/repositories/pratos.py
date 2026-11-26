from sqlmodel import Session, select

from app.domain.prato import Prato
from app.models import PratoDB


def criar(session: Session, prato: Prato) -> PratoDB:
    prato_db = PratoDB.de_dominio(prato)
    session.add(prato_db)
    session.commit()
    session.refresh(prato_db)
    return prato_db


def listar(session: Session) -> list[PratoDB]:
    return list(session.exec(select(PratoDB).order_by(PratoDB.nome)))


def buscar_por_id(session: Session, prato_id: int) -> PratoDB | None:
    return session.get(PratoDB, prato_id)
