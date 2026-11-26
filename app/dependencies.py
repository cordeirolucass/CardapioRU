from datetime import date, datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends
from sqlmodel import Session

from app.database import get_session

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


def hoje() -> date:
    """Data de hoje no fuso do RU (o servidor de produção roda em UTC)."""
    return datetime.now(FUSO_HORARIO).date()


SessionDep = Annotated[Session, Depends(get_session)]
HojeDep = Annotated[date, Depends(hoje)]
