from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from app.domain.avaliacao import Avaliacao


@dataclass(frozen=True)
class ItemRanking[T]:
    prato: T
    media: float
    total_avaliacoes: int


def media_avaliacoes(avaliacoes: Iterable[Avaliacao]) -> float | None:
    """Média das notas arredondada para 1 casa decimal, ou None se não houver avaliações."""
    notas = [avaliacao.nota for avaliacao in avaliacoes]
    if not notas:
        return None

    media = Decimal(sum(notas)) / Decimal(len(notas))
    return float(media.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def ranking_pratos[T](
    pratos_com_avaliacoes: Iterable[tuple[T, Sequence[Avaliacao]]],
) -> list[ItemRanking[T]]:
    """Ordena os pratos pela média (maior primeiro), desempatando pelo número de avaliações.

    Pratos sem avaliação ficam de fora. Em empate total, mantém a ordem recebida.
    """
    itens = []
    for prato, avaliacoes in pratos_com_avaliacoes:
        media = media_avaliacoes(avaliacoes)
        if media is not None:
            itens.append(ItemRanking(prato, media, len(avaliacoes)))

    return sorted(itens, key=lambda item: (item.media, item.total_avaliacoes), reverse=True)
