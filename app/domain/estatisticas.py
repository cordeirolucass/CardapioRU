from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal

from app.domain.avaliacao import Avaliacao


def media_avaliacoes(avaliacoes: Iterable[Avaliacao]) -> float | None:
    """Média das notas arredondada para 1 casa decimal, ou None se não houver avaliações."""
    notas = [avaliacao.nota for avaliacao in avaliacoes]
    if not notas:
        return None

    media = Decimal(sum(notas)) / Decimal(len(notas))
    return float(media.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
