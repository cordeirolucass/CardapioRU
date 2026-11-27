# CardapioRU

[![CI](https://github.com/cordeirolucass/CardapioRU/actions/workflows/ci.yml/badge.svg)](https://github.com/cordeirolucass/CardapioRU/actions/workflows/ci.yml)

Conheça o cardápio interativo e a avaliação de pratos do restaurante universitário mais gostoso da cidade.

**Acesse o app:** https://cardapioru-xu5v.onrender.com

> Hospedado no plano gratuito do Render: a primeira visita depois de um tempo parado pode levar até um minuto, enquanto o serviço acorda. As avaliações são apagadas a cada novo deploy, porque o banco SQLite não fica salvo nesse plano.

## Integrantes

- Lucas Oliveira Frade Ribeiro Cordeiro
- Olivier Menezes Vasconcelos
- Thiago Augusto Vaz Silveira

## Sobre o sistema

O CardapioRU mostra o cardápio do restaurante universitário e permite que os estudantes avaliem os pratos. O RU serve almoço e jantar de segunda a sexta.

Funcionalidades:

- **Cardápio de hoje** (`/`): almoço e jantar do dia, com a categoria de cada prato e a indicação dos vegetarianos.
- **Cardápio da semana** (`/semana`): uma tabela por dia útil, com filtro por categoria (prato principal, opção vegetariana, guarnição, salada e sobremesa) e opção de mostrar só os pratos vegetarianos.
- **Página do prato** (`/pratos/{id}`): calorias, média das notas, lista de avaliações e formulário para avaliar.
- **Avaliação de pratos**: nota de 1 a 5 e comentário opcional de até 280 caracteres. Um prato só pode ser avaliado no dia em que foi servido e até 3 dias depois.
- **Ranking** (`/ranking`): pratos ordenados pela média das notas. Em caso de empate, fica na frente o prato com mais avaliações.
- **API REST** (`/api/...`): os mesmos dados em JSON, com documentação interativa em `/docs`.

Ao iniciar com o banco vazio, o sistema cria um cardápio de exemplo para a semana atual, com algumas avaliações.

O código é organizado em camadas:

- `app/domain`: regras de negócio, sem dependência de banco ou web, como a validação da nota, o prazo de avaliação, a média e o ranking.
- `app/repositories`: acesso ao banco.
- `app/services`: casos de uso que combinam as regras e o banco, como registrar uma avaliação.
- `app/routers`: rotas da API e das páginas.
- `app/templates`: páginas HTML.

## Tecnologias

- **Python 3.12**
- **FastAPI**: rotas da API e das páginas, com documentação automática da API.
- **SQLModel** sobre **SQLite**: modelos e acesso ao banco.
- **Jinja2** e **Pico.css**: páginas HTML renderizadas no servidor, sem JavaScript próprio.
- **Uvicorn**: servidor da aplicação.
- **pytest** e **pytest-cov**: testes de unidade e de integração, com cobertura mínima de 80% exigida no CI.
- **Playwright**: testes end-to-end no navegador (Chromium).
- **Ruff**: lint e formatação do código.
- **GitHub Actions**: CI que roda lint, formatação, testes de unidade e testes e2e no Ubuntu, macOS e Windows.
- **Render**: hospedagem da aplicação.

## Uso de IA

Usamos o **Claude Code** como assistente ao longo do desenvolvimento:

- **Geração de código, testes e CI, com revisão humana:** a IA gerou parte do código das páginas, dos testes de unidade e e2e e dos passos do GitHub Actions. Todo o conteúdo gerado foi revisado pelo grupo antes de entrar no repositório.
- **Sugestão de testes para aumentar a cobertura:** a partir do relatório de cobertura, a IA apontou as linhas que nenhum teste executava e sugeriu testes para elas.
- **Entender melhor enunciados:** usamos a IA para esclarecer o que cada parte do enunciado pedia antes de começar a implementar.
- **Estimular ideias:** usamos a IA para levantar ideias e alternativas, que depois discutimos e escolhemos em grupo.

## Como executar localmente

Pré-requisitos: Python 3.12 ou superior e Git.

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/cordeirolucass/CardapioRU.git
   cd CardapioRU
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Linux/macOS: `source .venv/bin/activate`

3. Instale as dependências:

   ```bash
   pip install -r requirements-dev.txt
   ```

   Para rodar apenas a aplicação, sem as ferramentas de teste, basta `pip install -r requirements.txt`.

4. Inicie a aplicação:

   ```bash
   uvicorn app.main:app --reload
   ```

   Acesse em http://127.0.0.1:8000. A documentação interativa da API fica em http://127.0.0.1:8000/docs.

## Execução dos testes

Os comandos abaixo são executados na raiz do projeto, com o ambiente virtual ativado e as dependências de `requirements-dev.txt` instaladas (passos 2 e 3 acima).

### Testes de unidade

```bash
pytest tests/unit
```

Eles testam as regras de negócio, os repositórios, a API e as páginas HTML. Cada teste usa um banco SQLite em memória, então o `cardapioru.db` local não é alterado.

### Cobertura

```bash
pytest tests/unit --cov=app --cov-report=term-missing
```

O relatório mostra a porcentagem coberta de cada arquivo e, na coluna `Missing`, as linhas que nenhum teste executou. O CI falha se a cobertura total ficar abaixo de 80%. Para conferir isso localmente, acrescente `--cov-fail-under=80`.

Para ver o relatório linha a linha no navegador, gere a versão HTML e abra `htmlcov/index.html`:

```bash
pytest tests/unit --cov=app --cov-report=html
```

### Testes end-to-end (e2e)

Os testes e2e abrem o sistema num navegador de verdade, com o Playwright. Na primeira vez, instale o Chromium:

```bash
python -m playwright install chromium
```

Depois, rode:

```bash
pytest tests/e2e
```

Não é preciso iniciar a aplicação antes: os testes sobem o servidor sozinhos, numa porta livre e com um banco temporário, e o encerram no final.

Para ver o navegador funcionando durante os testes, use `pytest tests/e2e --headed --slowmo 500`.

O teste da página inicial é pulado aos sábados e domingos, porque o RU não serve refeições no fim de semana.

### Todos os testes

```bash
pytest
```

Roda os testes de unidade e os e2e juntos. Por isso, também exige o Chromium instalado.
