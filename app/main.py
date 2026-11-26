from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from app.database import criar_tabelas, engine
from app.dependencies import hoje
from app.routers import cardapio, pratos
from app.seed import popular_banco


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    criar_tabelas()
    with Session(engine) as session:
        popular_banco(session, hoje())
    yield


app = FastAPI(title="CardápioRU", lifespan=lifespan)
app.include_router(pratos.router)
app.include_router(cardapio.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
