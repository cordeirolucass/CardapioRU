import re

from playwright.sync_api import Page, expect

from app.dependencies import hoje
from app.domain.cardapio import dias_uteis_da_semana

# O seed monta a semana real, com almoço e jantar de 7 pratos em cada dia útil.
PRATOS_NA_SEMANA = 5 * 2 * 7


def test_navbar_leva_da_home_para_a_semana(page: Page, base_url: str):
    page.goto("/")

    page.get_by_test_id("nav-semana").click()

    expect(page).to_have_url(f"{base_url}/semana")
    expect(page).to_have_title(re.compile("Cardápio da semana"))
    expect(page.get_by_role("heading", name="Cardápio da semana", level=1)).to_be_visible()

    for dia in dias_uteis_da_semana(hoje()):
        expect(page.get_by_test_id(f"dia-{dia.isoformat()}")).to_be_visible()
    expect(page.get_by_role("table")).to_have_count(5)
    expect(page.get_by_test_id("prato")).to_have_count(PRATOS_NA_SEMANA)


def test_navbar_volta_da_semana_para_a_home(page: Page, base_url: str):
    page.goto("/semana")

    page.get_by_role("navigation").get_by_role("link", name="Hoje").click()

    expect(page).to_have_url(f"{base_url}/")
    expect(page.get_by_role("heading", name="Cardápio de hoje", level=1)).to_be_visible()
