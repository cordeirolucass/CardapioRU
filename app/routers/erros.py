from fastapi import status

from app.services.avaliacoes import ForaDoPrazo, PratoNaoEncontrado


def status_do_erro_de_avaliacao(erro: Exception) -> int:
    """Código HTTP para um erro levantado por registrar_avaliacao, igual na API e nas páginas."""
    if isinstance(erro, PratoNaoEncontrado):
        return status.HTTP_404_NOT_FOUND
    if isinstance(erro, ForaDoPrazo):
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_422_UNPROCESSABLE_CONTENT
