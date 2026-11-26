from app.domain.avaliacao import Avaliacao
from app.domain.estatisticas import media_avaliacoes


def avaliacoes_com_notas(*notas):
    return [Avaliacao(nota=nota) for nota in notas]


def test_media_sem_avaliacoes_e_none():
    assert media_avaliacoes([]) is None


def test_media_de_uma_avaliacao_e_a_propria_nota():
    assert media_avaliacoes(avaliacoes_com_notas(4)) == 4.0


def test_media_de_varias_avaliacoes():
    assert media_avaliacoes(avaliacoes_com_notas(5, 3, 4)) == 4.0


def test_media_e_arredondada_para_uma_casa_decimal():
    assert media_avaliacoes(avaliacoes_com_notas(5, 4, 4)) == 4.3


def test_media_terminada_em_cinco_e_arredondada_para_cima():
    assert media_avaliacoes(avaliacoes_com_notas(4, 4, 4, 5)) == 4.3
