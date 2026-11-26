import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[2]
HOST = "127.0.0.1"
TEMPO_MAXIMO_SUBIDA = 30  # segundos


def porta_livre() -> int:
    """Pede ao sistema uma porta livre. Ela é liberada logo em seguida para o uvicorn usar."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def esperar_health(url: str, processo: subprocess.Popen, log: Path) -> None:
    """Espera o /health responder 200, falhando se o servidor morrer ou demorar demais."""
    limite = time.monotonic() + TEMPO_MAXIMO_SUBIDA
    while time.monotonic() < limite:
        if processo.poll() is not None:
            pytest.fail(
                f"O uvicorn encerrou com código {processo.returncode} antes de responder.\n"
                f"{log.read_text(encoding='utf-8', errors='replace')}"
            )
        try:
            with urllib.request.urlopen(f"{url}/health", timeout=1) as resposta:
                if resposta.status == 200:
                    return
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pass
        time.sleep(0.2)

    pytest.fail(
        f"O /health não respondeu em {TEMPO_MAXIMO_SUBIDA}s.\n"
        f"{log.read_text(encoding='utf-8', errors='replace')}"
    )


def encerrar(processo: subprocess.Popen) -> None:
    if processo.poll() is not None:
        return
    processo.terminate()
    try:
        processo.wait(timeout=10)
    except subprocess.TimeoutExpired:
        processo.kill()
        processo.wait()


@pytest.fixture(scope="session")
def servidor(tmp_path_factory) -> str:
    """Sobe a aplicação com uvicorn num subprocesso e devolve a URL base, como
    "http://127.0.0.1:54321".

    Usa uma porta livre e um banco SQLite temporário, populado pelo seed na subida. O servidor
    é encerrado no final da sessão de testes. A saída do uvicorn fica em uvicorn.log, na pasta
    temporária, e aparece na mensagem de erro se ele não subir.
    """
    pasta = tmp_path_factory.mktemp("servidor_e2e")
    banco = pasta / "cardapioru_e2e.db"
    log = pasta / "uvicorn.log"
    porta = porta_livre()
    url = f"http://{HOST}:{porta}"

    env = os.environ | {"DATABASE_URL": f"sqlite:///{banco.as_posix()}"}
    comando = [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", HOST, "--port", str(porta),
    ]  # fmt: skip

    with log.open("w", encoding="utf-8") as saida:
        processo = subprocess.Popen(
            comando, cwd=RAIZ_DO_PROJETO, env=env, stdout=saida, stderr=subprocess.STDOUT
        )
        try:
            esperar_health(url, processo, log)
            yield url
        finally:
            encerrar(processo)


@pytest.fixture(scope="session")
def base_url(servidor) -> str:
    """Faz o page.goto("/") do pytest-playwright apontar para o servidor de teste."""
    return servidor
