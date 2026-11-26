from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import HojeDep, SessionDep
from app.domain.filtros import filtrar_pratos
from app.domain.prato import Categoria
from app.repositories import pratos as repo_pratos
from app.routers.erros import status_do_erro_de_avaliacao
from app.schemas import AvaliacaoEntrada, AvaliacaoPublica, PratoPublico
from app.services.avaliacoes import ForaDoPrazo, PratoNaoEncontrado, registrar_avaliacao

router = APIRouter(prefix="/api/pratos", tags=["pratos"])


@router.get("")
def listar_pratos(
    session: SessionDep,
    categoria: Annotated[Categoria | None, Query()] = None,
    vegetariano: Annotated[bool, Query()] = False,
) -> list[PratoPublico]:
    pratos = filtrar_pratos(
        repo_pratos.listar(session), categoria=categoria, apenas_vegetarianos=vegetariano
    )
    return [PratoPublico.de_db(prato) for prato in pratos]


@router.post("/{prato_id}/avaliacoes", status_code=status.HTTP_201_CREATED)
def avaliar_prato(
    prato_id: int, entrada: AvaliacaoEntrada, session: SessionDep, hoje: HojeDep
) -> AvaliacaoPublica:
    try:
        criada = registrar_avaliacao(session, prato_id, entrada.nota, entrada.comentario, hoje)
    except PratoNaoEncontrado as erro:
        raise HTTPException(status_do_erro_de_avaliacao(erro), "Prato não encontrado.") from None
    except (ValueError, ForaDoPrazo) as erro:
        raise HTTPException(status_do_erro_de_avaliacao(erro), str(erro)) from None

    return AvaliacaoPublica.model_validate(criada, from_attributes=True)
