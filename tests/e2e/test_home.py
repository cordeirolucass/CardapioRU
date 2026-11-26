import re

import pytest
from playwright.sync_api import Page, expect

from app.dependencies import hoje
from app.seed import CARDAPIO

# O servidor de teste é populado pelo seed, que monta o cardápio da semana real
# (segunda a sexta). Por isso o teste usa a data de hoje no fuso do RU, igual ao servidor.
HOJE = hoje()

pytestmark = pytest.mark.skipif(
    HOJE.weekday() >= 5, reason="O RU não serve refeições no fim de semana."
)


def test_home_mostra_almoco_e_jantar_de_hoje(page: Page):
    principal_almoco, principal_jantar, *_ = CARDAPIO[HOJE.weekday()]

    page.goto("/")

    expect(page).to_have_title(re.compile("Cardápio de hoje"))
    expect(page.get_by_role("heading", name="Cardápio de hoje", level=1)).to_be_visible()
    expect(page.get_by_test_id("sem-cardapio")).to_have_count(0)

    almoco = page.get_by_test_id("refeicao-almoco")
    expect(almoco.get_by_role("heading", name="Almoço")).to_be_visible()
    expect(almoco.get_by_role("link", name=principal_almoco)).to_be_visible()
    expect(almoco.get_by_test_id("prato")).to_have_count(7)

    jantar = page.get_by_test_id("refeicao-jantar")
    expect(jantar.get_by_role("heading", name="Jantar")).to_be_visible()
    expect(jantar.get_by_role("link", name=principal_jantar)).to_be_visible()
    expect(jantar.get_by_test_id("prato")).to_have_count(7)
