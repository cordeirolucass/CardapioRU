from fastapi import APIRouter

from app.dependencies import HojeDep, SessionDep
from app.domain.cardapio import cardapio_da_semana
from app.repositories import refeicoes as repo_refeicoes
from app.schemas import CardapioDaSemana, CardapioDoDia, RefeicaoPublica

router = APIRouter(prefix="/api/cardapio", tags=["cardápio"])


@router.get("/hoje")
def cardapio_de_hoje(session: SessionDep, hoje: HojeDep) -> CardapioDoDia:
    refeicoes = repo_refeicoes.listar_por_data(session, hoje)
    return CardapioDoDia(data=hoje, refeicoes=[RefeicaoPublica.de_db(r) for r in refeicoes])


@router.get("/semana")
def cardapio_semanal(session: SessionDep, hoje: HojeDep) -> CardapioDaSemana:
    semana = cardapio_da_semana(repo_refeicoes.listar_da_semana(session, hoje), hoje)
    return CardapioDaSemana(
        dias=[
            CardapioDoDia(data=dia, refeicoes=[RefeicaoPublica.de_db(r) for r in refeicoes])
            for dia, refeicoes in semana.items()
        ]
    )
