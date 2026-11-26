# CardapioRU
Conheça o cardápio interativo e a avaliação de pratos do restaurante universitário mais gostoso da cidade.

## Integrantes

- Lucas Oliveira Frade Ribeiro Cordeiro
- Olivier Menezes Vasconcelos
- Thiago Augusto Vaz Silveira

## Sobre o sistema

## Tecnologias

## Uso de IA

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
