from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import HojeDep, SessionDep
from app.domain.avaliacao import Avaliacao, pode_avaliar
from app.domain.filtros import filtrar_pratos
from app.domain.prato import Categoria
from app.repositories import avaliacoes as repo_avaliacoes
from app.repositories import pratos as repo_pratos
from app.repositories import refeicoes as repo_refeicoes
from app.schemas import AvaliacaoEntrada, AvaliacaoPublica, PratoPublico

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
    if repo_pratos.buscar_por_id(session, prato_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Prato não encontrado.")

    try:
        avaliacao = Avaliacao(entrada.nota, entrada.comentario)
    except ValueError as erro:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(erro)) from None

    servido_em = repo_refeicoes.ultima_data_servida(session, prato_id, ate=hoje)
    if servido_em is None or not pode_avaliar(servido_em, hoje):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Este prato só pode ser avaliado até 3 dias depois de ser servido.",
        )

    criada = repo_avaliacoes.criar(session, prato_id, avaliacao, criada_em=hoje)
    return AvaliacaoPublica.model_validate(criada, from_attributes=True)
