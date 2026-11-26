import re

from playwright.sync_api import Page, expect

from app.seed import PRATOS

PRATOS_NAO_VEGETARIANOS = [prato.nome for prato in PRATOS if not prato.e_vegetariano]

# No seed, cada refeição tem 1 prato principal não vegetariano e 6 acompanhamentos vegetarianos,
# em almoço e jantar dos 5 dias úteis.
PRATOS_NA_SEMANA = 5 * 2 * 7
PRATOS_VEGETARIANOS_NA_SEMANA = 5 * 2 * 6


def test_filtro_vegetariano_mostra_so_pratos_vegetarianos(page: Page):
    page.goto("/semana")
    expect(page.get_by_test_id("prato")).to_have_count(PRATOS_NA_SEMANA)

    filtro = page.get_by_test_id("form-filtro")
    filtro.get_by_role("checkbox", name="Só vegetarianos").check()
    filtro.get_by_role("button", name="Filtrar").click()

    expect(page).to_have_url(re.compile(r"/semana\?.*vegetariano=true"))
    expect(page.get_by_role("checkbox", name="Só vegetarianos")).to_be_checked()

    pratos = page.get_by_test_id("prato")
    expect(pratos).to_have_count(PRATOS_VEGETARIANOS_NA_SEMANA)
    expect(pratos.filter(has_not_text="🌱 vegetariano")).to_have_count(0)
    for nome in PRATOS_NAO_VEGETARIANOS:
        expect(page.get_by_role("link", name=nome, exact=True)).to_have_count(0)


def test_limpar_filtro_volta_a_mostrar_todos_os_pratos(page: Page, base_url: str):
    page.goto("/semana?vegetariano=true")
    expect(page.get_by_test_id("prato")).to_have_count(PRATOS_VEGETARIANOS_NA_SEMANA)

    page.get_by_test_id("limpar-filtro").click()

    expect(page).to_have_url(f"{base_url}/semana")
    expect(page.get_by_role("checkbox", name="Só vegetarianos")).not_to_be_checked()
    expect(page.get_by_test_id("prato")).to_have_count(PRATOS_NA_SEMANA)
    expect(page.get_by_test_id("limpar-filtro")).to_have_count(0)
