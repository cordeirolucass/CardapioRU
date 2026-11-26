from datetime import date

from pydantic import BaseModel

from app.models import PratoDB, RefeicaoDB, TipoRefeicao


class PratoPublico(BaseModel):
    id: int
    nome: str
    categoria: str
    calorias: int
    vegetariano: bool

    @classmethod
    def de_db(cls, prato: PratoDB) -> "PratoPublico":
        return cls(
            id=prato.id,
            nome=prato.nome,
            categoria=prato.categoria,
            calorias=prato.calorias,
            vegetariano=prato.e_vegetariano,
        )


class RefeicaoPublica(BaseModel):
    tipo: TipoRefeicao
    pratos: list[PratoPublico]

    @classmethod
    def de_db(cls, refeicao: RefeicaoDB) -> "RefeicaoPublica":
        return cls(tipo=refeicao.tipo, pratos=[PratoPublico.de_db(p) for p in refeicao.pratos])


class CardapioDoDia(BaseModel):
    data: date
    refeicoes: list[RefeicaoPublica]


class CardapioDaSemana(BaseModel):
    dias: list[CardapioDoDia]


class AvaliacaoEntrada(BaseModel):
    nota: int
    comentario: str | None = None


class AvaliacaoPublica(BaseModel):
    id: int
    nota: int
    comentario: str | None
    criada_em: date
