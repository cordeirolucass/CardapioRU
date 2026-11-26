from fastapi import FastAPI

app = FastAPI(title="CardápioRU")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
