from collections.abc import Iterable

from app.domain.prato import Categoria, Prato


def filtrar_pratos(
    pratos: Iterable[Prato],
    categoria: Categoria | str | None = None,
    apenas_vegetarianos: bool = False,
) -> list[Prato]:
    """Filtra os pratos por categoria e/ou apenas vegetarianos. Sem filtros, retorna todos."""
    if categoria is not None:
        categoria = Categoria(categoria)

    return [
        prato
        for prato in pratos
        if (categoria is None or prato.categoria == categoria)
        and (not apenas_vegetarianos or prato.e_vegetariano)
    ]
