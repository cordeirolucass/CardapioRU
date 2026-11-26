from sqlmodel import Session

from app.domain.estatisticas import ItemRanking, ranking_pratos
from app.models import PratoDB
from app.repositories import pratos as repo_pratos


def ranking_atual(session: Session) -> list[ItemRanking[PratoDB]]:
    """Ranking de todos os pratos avaliados, do melhor para o pior."""
    return ranking_pratos((prato, prato.avaliacoes) for prato in repo_pratos.listar(session))
