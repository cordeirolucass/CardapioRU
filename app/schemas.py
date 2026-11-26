from pydantic import BaseModel

from app.models import PratoDB


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
