from dataclasses import dataclass
from enum import StrEnum


class Categoria(StrEnum):
    PRINCIPAL = "principal"
    VEGETARIANO = "vegetariano"
    GUARNICAO = "guarnicao"
    SALADA = "salada"
    SOBREMESA = "sobremesa"


@dataclass(frozen=True)
class Prato:
    nome: str
    categoria: Categoria | str
    calorias: int
    vegetariano: bool = False

    def __post_init__(self) -> None:
        nome = self.nome.strip()
        if not nome:
            raise ValueError("O nome do prato não pode ser vazio.")

        try:
            categoria = Categoria(self.categoria)
        except ValueError:
            opcoes = ", ".join(c.value for c in Categoria)
            raise ValueError(
                f"Categoria inválida: {self.categoria!r}. Use uma de: {opcoes}."
            ) from None

        if self.calorias < 0:
            raise ValueError("As calorias não podem ser negativas.")

        object.__setattr__(self, "nome", nome)
        object.__setattr__(self, "categoria", categoria)

    @property
    def e_vegetariano(self) -> bool:
        return self.vegetariano or self.categoria == Categoria.VEGETARIANO
