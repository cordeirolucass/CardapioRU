from datetime import date
from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel

from app.domain.prato import Categoria, Prato


class TipoRefeicao(StrEnum):
    ALMOCO = "almoco"
    JANTAR = "jantar"


class RefeicaoPratoLink(SQLModel, table=True):
    refeicao_id: int | None = Field(default=None, foreign_key="refeicaodb.id", primary_key=True)
    prato_id: int | None = Field(default=None, foreign_key="pratodb.id", primary_key=True)


class PratoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    categoria: str
    calorias: int
    vegetariano: bool = False

    refeicoes: list["RefeicaoDB"] = Relationship(
        back_populates="pratos", link_model=RefeicaoPratoLink
    )
    avaliacoes: list["AvaliacaoDB"] = Relationship(back_populates="prato")

    @property
    def e_vegetariano(self) -> bool:
        return self.vegetariano or self.categoria == Categoria.VEGETARIANO

    @classmethod
    def de_dominio(cls, prato: Prato) -> "PratoDB":
        return cls(
            nome=prato.nome,
            categoria=str(prato.categoria),
            calorias=prato.calorias,
            vegetariano=prato.vegetariano,
        )


class RefeicaoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: date = Field(index=True)
    tipo: TipoRefeicao

    pratos: list[PratoDB] = Relationship(back_populates="refeicoes", link_model=RefeicaoPratoLink)


class AvaliacaoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    prato_id: int = Field(foreign_key="pratodb.id", index=True)
    nota: int
    comentario: str | None = None
    criada_em: date

    prato: PratoDB | None = Relationship(back_populates="avaliacoes")
