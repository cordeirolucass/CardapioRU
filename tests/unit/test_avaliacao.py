import pytest

from app.domain.avaliacao import Avaliacao


@pytest.mark.parametrize("nota", [1, 5])
def test_notas_nos_limites_sao_aceitas(nota):
    avaliacao = Avaliacao(nota=nota)

    assert avaliacao.nota == nota


@pytest.mark.parametrize("nota", [0, 6])
def test_notas_fora_do_intervalo_sao_rejeitadas(nota):
    with pytest.raises(ValueError, match="entre 1 e 5"):
        Avaliacao(nota=nota)


@pytest.mark.parametrize("nota", [4.5, "5", True])
def test_nota_que_nao_e_inteiro_e_rejeitada(nota):
    with pytest.raises(ValueError, match="inteiro"):
        Avaliacao(nota=nota)


def test_comentario_com_280_caracteres_e_aceito():
    comentario = "a" * 280

    avaliacao = Avaliacao(nota=4, comentario=comentario)

    assert avaliacao.comentario == comentario


def test_comentario_com_mais_de_280_caracteres_e_rejeitado():
    with pytest.raises(ValueError, match="280 caracteres"):
        Avaliacao(nota=4, comentario="a" * 281)


def test_comentario_em_branco_e_tratado_como_ausente():
    avaliacao = Avaliacao(nota=3, comentario="   ")

    assert avaliacao.comentario is None
