from dataclasses import dataclass

NOTA_MINIMA = 1
NOTA_MAXIMA = 5
TAMANHO_MAXIMO_COMENTARIO = 280


@dataclass(frozen=True)
class Avaliacao:
    nota: int
    comentario: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.nota, bool) or not isinstance(self.nota, int):
            raise ValueError("A nota deve ser um número inteiro.")

        if not NOTA_MINIMA <= self.nota <= NOTA_MAXIMA:
            raise ValueError(f"A nota deve estar entre {NOTA_MINIMA} e {NOTA_MAXIMA}.")

        comentario = (self.comentario or "").strip() or None
        if comentario is not None and len(comentario) > TAMANHO_MAXIMO_COMENTARIO:
            raise ValueError(
                f"O comentário deve ter no máximo {TAMANHO_MAXIMO_COMENTARIO} caracteres."
            )

        object.__setattr__(self, "comentario", comentario)
