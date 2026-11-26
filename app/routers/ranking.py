from fastapi import APIRouter

from app.dependencies import SessionDep
from app.domain.estatisticas import ranking_pratos
from app.repositories import pratos as repo_pratos
from app.schemas import ItemRankingPublico, PratoPublico

router = APIRouter(prefix="/api/ranking", tags=["ranking"])


@router.get("")
def ranking(session: SessionDep) -> list[ItemRankingPublico]:
    itens = ranking_pratos((prato, prato.avaliacoes) for prato in repo_pratos.listar(session))
    return [
        ItemRankingPublico(
            posicao=posicao,
            prato=PratoPublico.de_db(item.prato),
            media=item.media,
            total_avaliacoes=item.total_avaliacoes,
        )
        for posicao, item in enumerate(itens, start=1)
    ]
