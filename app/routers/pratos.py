from typing import Annotated

from fastapi import APIRouter, Query

from app.dependencies import SessionDep
from app.domain.filtros import filtrar_pratos
from app.domain.prato import Categoria
from app.repositories import pratos as repo_pratos
from app.schemas import PratoPublico

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
