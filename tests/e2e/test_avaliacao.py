import re

from playwright.sync_api import Page, expect

# Guarnição servida no almoço e no jantar de todo dia útil do seed. Assim ela está sempre
# dentro do prazo de 3 dias para avaliar, inclusive no sábado e no domingo (servida na sexta).
PRATO = "Arroz branco"
COMENTARIO = "Soltinho e no ponto, avaliado pelo teste e2e."


def test_avaliar_prato_com_nota_5_e_comentario(page: Page):
    page.goto("/semana")
    page.get_by_role("link", name=PRATO).first.click()

    expect(page).to_have_url(re.compile(r"/pratos/\d+$"))
    expect(page.get_by_role("heading", name=PRATO, level=1)).to_be_visible()

    formulario = page.get_by_test_id("form-avaliacao")
    formulario.get_by_test_id("nota-5").check()
    formulario.get_by_label("Comentário").fill(COMENTARIO)
    formulario.get_by_role("button", name="Enviar avaliação").click()

    expect(page).to_have_url(re.compile(r"/pratos/\d+\?avaliado=true$"))
    expect(page.get_by_test_id("avaliacao-enviada")).to_have_text(
        "Obrigado! Sua avaliação foi registrada."
    )
    expect(page.get_by_test_id("erro-avaliacao")).to_have_count(0)

    minha_avaliacao = page.get_by_test_id("avaliacao").filter(has_text=COMENTARIO)
    expect(minha_avaliacao).to_have_count(1)
    expect(minha_avaliacao.get_by_test_id("avaliacao-nota")).to_have_text("5")
