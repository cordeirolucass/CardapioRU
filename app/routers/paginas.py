from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.dependencies import HojeDep, SessionDep
from app.domain.cardapio import cardapio_da_semana
from app.repositories import refeicoes as repo_refeicoes
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
