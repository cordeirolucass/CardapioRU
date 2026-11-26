from datetime import date

from sqlmodel import Session

from app.domain.avaliacao import Avaliacao, pode_avaliar
from app.models import AvaliacaoDB
from app.repositories import avaliacoes as repo_avaliacoes
from app.repositories import pratos as repo_pratos
from app.repositories import refeicoes as repo_refeicoes

MENSAGEM_FORA_DO_PRAZO = "Este prato só pode ser avaliado até 3 dias depois de ser servido."


class PratoNaoEncontrado(Exception):
    pass


class ForaDoPrazo(Exception):
    pass


def esta_no_prazo(session: Session, prato_id: int, hoje: date) -> bool:
    """Se o prato foi servido recentemente o bastante para ainda poder ser avaliado."""
    servido_em = repo_refeicoes.ultima_data_servida(session, prato_id, ate=hoje)
    return servido_em is not None and pode_avaliar(servido_em, hoje)


def registrar_avaliacao(
    session: Session, prato_id: int, nota: int, comentario: str | None, hoje: date
) -> AvaliacaoDB:
    """Valida e grava uma avaliação.

    Levanta PratoNaoEncontrado, ValueError (nota ou comentário inválidos) ou ForaDoPrazo.
    """
    if repo_pratos.buscar_por_id(session, prato_id) is None:
        raise PratoNaoEncontrado

    avaliacao = Avaliacao(nota, comentario)

    if not esta_no_prazo(session, prato_id, hoje):
        raise ForaDoPrazo(MENSAGEM_FORA_DO_PRAZO)

    return repo_avaliacoes.criar(session, prato_id, avaliacao, criada_em=hoje)
