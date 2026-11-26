from fastapi import APIRouter

from app.dependencies import SessionDep
from app.schemas import ItemRankingPublico, PratoPublico
from app.services.ranking import ranking_atual

router = APIRouter(prefix="/api/ranking", tags=["ranking"])


@router.get("")
def ranking(session: SessionDep) -> list[ItemRankingPublico]:
    return [
        ItemRankingPublico(
            posicao=posicao,
            prato=PratoPublico.de_db(item.prato),
            media=item.media,
            total_avaliacoes=item.total_avaliacoes,
        )
        for posicao, item in enumerate(ranking_atual(session), start=1)
    ]
