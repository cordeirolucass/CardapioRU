import re

from playwright.sync_api import Page, expect

# Guarnição servida no almoço e no jantar de todo dia útil do seed. Assim ela está sempre
# dentro do prazo de 3 dias para avaliar, inclusive no sábado e no domingo (servida na sexta).
PRATO = "Arroz branco"
COMENTARIO = "Soltinho e no ponto, avaliado pelo teste e2e."


def abrir_prato(page: Page) -> None:
    page.goto("/semana")
    page.get_by_role("link", name=PRATO).first.click()
    expect(page.get_by_role("heading", name=PRATO, level=1)).to_be_visible()


def test_avaliar_prato_com_nota_5_e_comentario(page: Page):
    abrir_prato(page)
    expect(page).to_have_url(re.compile(r"/pratos/\d+$"))

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


def test_navegador_nao_envia_sem_nota(page: Page):
    abrir_prato(page)
    url_do_prato = page.url

    formulario = page.get_by_test_id("form-avaliacao")
    formulario.get_by_label("Comentário").fill("Esqueci a nota")
    formulario.get_by_role("button", name="Enviar avaliação").click()

    # O campo de nota é obrigatório: o navegador barra o envio e continua na mesma página.
    expect(page).to_have_url(url_do_prato)
    expect(formulario.get_by_test_id("nota-1")).to_have_js_property("validity.valid", False)


def test_enviar_sem_nota_mostra_erro_e_mantem_o_comentario(page: Page):
    comentario = "Sem nota, enviado pelo teste e2e."
    abrir_prato(page)

    formulario = page.get_by_test_id("form-avaliacao")
    # Desliga a validação do navegador para o pedido chegar ao servidor sem nota, como
    # aconteceria num navegador antigo ou com o HTML alterado.
    formulario.evaluate("form => { form.noValidate = true; }")
    formulario.get_by_label("Comentário").fill(comentario)
    formulario.get_by_role("button", name="Enviar avaliação").click()

    expect(page.get_by_test_id("erro-avaliacao")).to_have_text("Escolha uma nota de 1 a 5.")
    expect(page.get_by_role("alert")).to_be_visible()
    expect(page.get_by_test_id("avaliacao-enviada")).to_have_count(0)
    expect(page.get_by_label("Comentário")).to_have_value(comentario)
    expect(page.get_by_test_id("avaliacao").filter(has_text=comentario)).to_have_count(0)
