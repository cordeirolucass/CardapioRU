"""Cardápio de exemplo, inserido ao iniciar o app quando o banco está vazio."""

from datetime import date

from sqlmodel import Session, select

from app.domain.avaliacao import Avaliacao
from app.domain.cardapio import dias_uteis_da_semana
from app.domain.prato import Prato
from app.models import PratoDB, TipoRefeicao
from app.repositories import avaliacoes, pratos, refeicoes

PRATOS = [
    Prato("Frango grelhado", "principal", 420),
    Prato("Carne de panela", "principal", 510),
    Prato("Peixe assado", "principal", 380),
    Prato("Feijoada", "principal", 750),
    Prato("Strogonoff de cogumelos", "vegetariano", 450),
    Prato("Lentilha com legumes", "vegetariano", 390),
    Prato("Arroz branco", "guarnicao", 210, vegetariano=True),
    Prato("Feijão carioca", "guarnicao", 180, vegetariano=True),
    Prato("Farofa de couve", "guarnicao", 160, vegetariano=True),
    Prato("Salada verde", "salada", 40, vegetariano=True),
    Prato("Salada de tomate", "salada", 35, vegetariano=True),
    Prato("Pudim", "sobremesa", 300, vegetariano=True),
    Prato("Banana", "sobremesa", 90, vegetariano=True),
]

# Para cada dia útil: (prato principal do almoço, do jantar, opção vegetariana, salada, sobremesa)
CARDAPIO = [
    ("Frango grelhado", "Carne de panela", "Lentilha com legumes", "Salada verde", "Banana"),
    ("Carne de panela", "Peixe assado", "Strogonoff de cogumelos", "Salada de tomate", "Pudim"),
    ("Feijoada", "Frango grelhado", "Lentilha com legumes", "Salada verde", "Banana"),
    ("Peixe assado", "Carne de panela", "Strogonoff de cogumelos", "Salada de tomate", "Banana"),
    ("Frango grelhado", "Feijoada", "Lentilha com legumes", "Salada verde", "Pudim"),
]
GUARNICOES = ["Arroz branco", "Feijão carioca", "Farofa de couve"]

AVALIACOES = [
    ("Feijoada", 5, "Melhor dia da semana!"),
    ("Feijoada", 4, None),
    ("Strogonoff de cogumelos", 5, "Muito bem temperado."),
    ("Frango grelhado", 3, "Um pouco seco."),
    ("Pudim", 4, None),
]


def popular_banco(session: Session, hoje: date) -> bool:
    """Insere o cardápio de exemplo da semana de hoje se ainda não houver pratos.

    Retorna True se inseriu os dados e False se o banco já estava populado.
    """
    if session.exec(select(PratoDB)).first() is not None:
        return False

    por_nome = {prato.nome: pratos.criar(session, prato) for prato in PRATOS}
    guarnicoes = [por_nome[nome] for nome in GUARNICOES]

    for dia, (almoco, jantar, vegetariano, salada, sobremesa) in zip(
        dias_uteis_da_semana(hoje), CARDAPIO, strict=True
    ):
        acompanhamentos = [
            por_nome[vegetariano],
            *guarnicoes,
            por_nome[salada],
            por_nome[sobremesa],
        ]
        refeicoes.criar(session, dia, TipoRefeicao.ALMOCO, [por_nome[almoco], *acompanhamentos])
        refeicoes.criar(session, dia, TipoRefeicao.JANTAR, [por_nome[jantar], *acompanhamentos])

    for nome, nota, comentario in AVALIACOES:
        avaliacoes.criar(session, por_nome[nome].id, Avaliacao(nota, comentario), criada_em=hoje)

    return True
