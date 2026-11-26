from fastapi import APIRouter

from app.dependencies import HojeDep, SessionDep
from app.repositories import refeicoes as repo_refeicoes
from app.schemas import CardapioDaSemana, CardapioDoDia
from app.services.cardapio import semana_de

router = APIRouter(prefix="/api/cardapio", tags=["cardápio"])


@router.get("/hoje")
def cardapio_de_hoje(session: SessionDep, hoje: HojeDep) -> CardapioDoDia:
    return CardapioDoDia.de_db(hoje, repo_refeicoes.listar_por_data(session, hoje))


@router.get("/semana")
def cardapio_semanal(session: SessionDep, hoje: HojeDep) -> CardapioDaSemana:
    return CardapioDaSemana(
        dias=[
            CardapioDoDia.de_db(dia, refeicoes)
            for dia, refeicoes in semana_de(session, hoje).items()
        ]
    )
