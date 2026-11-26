from datetime import date
from typing import Annotated

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session

from app.dependencies import HojeDep, SessionDep
from app.domain.avaliacao import NOTA_MAXIMA, NOTA_MINIMA, TAMANHO_MAXIMO_COMENTARIO
from app.domain.cardapio import cardapio_da_semana
from app.domain.estatisticas import media_avaliacoes
from app.models import PratoDB
from app.repositories import avaliacoes as repo_avaliacoes
from app.repositories import pratos as repo_pratos
from app.repositories import refeicoes as repo_refeicoes
from app.services.avaliacoes import (
    ForaDoPrazo,
    PratoNaoEncontrado,
    esta_no_prazo,
    registrar_avaliacao,
)
from app.web import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request, session: SessionDep, hoje: HojeDep):
    refeicoes = repo_refeicoes.listar_por_data(session, hoje)
    return templates.TemplateResponse(request, "hoje.html", {"hoje": hoje, "refeicoes": refeicoes})


@router.get("/semana", response_class=HTMLResponse)
def pagina_semana(request: Request, session: SessionDep, hoje: HojeDep):
    semana = cardapio_da_semana(repo_refeicoes.listar_da_semana(session, hoje), hoje)
    return templates.TemplateResponse(request, "semana.html", {"hoje": hoje, "semana": semana})


def _pagina_nao_encontrada(request: Request):
    return templates.TemplateResponse(
        request, "nao_encontrado.html", status_code=status.HTTP_404_NOT_FOUND
    )


def _pagina_prato(
    request: Request,
    session: Session,
    prato: PratoDB,
    hoje: date,
    *,
    erro: str | None = None,
    nota: str | None = None,
    comentario: str | None = None,
    avaliado: bool = False,
    status_code: int = status.HTTP_200_OK,
):
    avaliacoes = repo_avaliacoes.listar_por_prato(session, prato.id)
    contexto = {
        "prato": prato,
        "avaliacoes": avaliacoes,
        "media": media_avaliacoes(avaliacoes),
        "pode_avaliar": esta_no_prazo(session, prato.id, hoje),
        "notas": range(NOTA_MAXIMA, NOTA_MINIMA - 1, -1),
        "tamanho_maximo_comentario": TAMANHO_MAXIMO_COMENTARIO,
        "erro": erro,
        "nota": nota,
        "comentario": comentario,
        "avaliado": avaliado,
    }
    return templates.TemplateResponse(request, "prato.html", contexto, status_code=status_code)


@router.get("/pratos/{prato_id}", response_class=HTMLResponse)
def pagina_prato(
    request: Request, prato_id: int, session: SessionDep, hoje: HojeDep, avaliado: bool = False
):
    prato = repo_pratos.buscar_por_id(session, prato_id)
    if prato is None:
        return _pagina_nao_encontrada(request)
    return _pagina_prato(request, session, prato, hoje, avaliado=avaliado)


@router.post("/pratos/{prato_id}/avaliacoes", response_class=HTMLResponse)
def enviar_avaliacao(
    request: Request,
    prato_id: int,
    session: SessionDep,
    hoje: HojeDep,
    nota: Annotated[str | None, Form()] = None,
    comentario: Annotated[str | None, Form()] = None,
):
    prato = repo_pratos.buscar_por_id(session, prato_id)
    if prato is None:
        return _pagina_nao_encontrada(request)

    try:
        if not (nota and nota.strip().isdigit()):
            raise ValueError(f"Escolha uma nota de {NOTA_MINIMA} a {NOTA_MAXIMA}.")
        registrar_avaliacao(session, prato_id, int(nota), comentario, hoje)
    except PratoNaoEncontrado:
        return _pagina_nao_encontrada(request)
    except (ValueError, ForaDoPrazo) as erro:
        codigo = (
            status.HTTP_400_BAD_REQUEST
            if isinstance(erro, ForaDoPrazo)
            else status.HTTP_422_UNPROCESSABLE_CONTENT
        )
        return _pagina_prato(
            request,
            session,
            prato,
            hoje,
            erro=str(erro),
            nota=nota,
            comentario=comentario,
            status_code=codigo,
        )

    return RedirectResponse(
        f"/pratos/{prato_id}?avaliado=true", status_code=status.HTTP_303_SEE_OTHER
    )
