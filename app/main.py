from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI
from sqlmodel import Session

from app.database import criar_tabelas, engine
from app.seed import popular_banco


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    criar_tabelas()
    with Session(engine) as session:
        popular_banco(session, date.today())
    yield


app = FastAPI(title="CardápioRU", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
