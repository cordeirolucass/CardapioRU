from pathlib import Path

from fastapi.templating import Jinja2Templates

PASTA_TEMPLATES = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=PASTA_TEMPLATES)

NOMES_TIPO_REFEICAO = {"almoco": "Almoço", "jantar": "Jantar"}
NOMES_CATEGORIA = {
    "principal": "Prato principal",
    "vegetariano": "Opção vegetariana",
    "guarnicao": "Guarnição",
    "salada": "Salada",
    "sobremesa": "Sobremesa",
}
DIAS_DA_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

templates.env.filters["tipo_refeicao"] = lambda tipo: NOMES_TIPO_REFEICAO.get(str(tipo), tipo)
templates.env.filters["categoria"] = lambda categoria: NOMES_CATEGORIA.get(categoria, categoria)
templates.env.filters["data_br"] = lambda data: data.strftime("%d/%m/%Y")
templates.env.filters["dia_da_semana"] = lambda data: DIAS_DA_SEMANA[data.weekday()]
