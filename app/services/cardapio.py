from datetime import date

from sqlmodel import Session

from app.domain.cardapio import cardapio_da_semana
from app.models import RefeicaoDB
from app.repositories import refeicoes as repo_refeicoes


def semana_de(session: Session, hoje: date) -> dict[date, list[RefeicaoDB]]:
    """Refeições da semana de hoje agrupadas por dia útil, de segunda a sexta."""
    return cardapio_da_semana(repo_refeicoes.listar_da_semana(session, hoje), hoje)
