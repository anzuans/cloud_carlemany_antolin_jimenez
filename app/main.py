from fastapi import FastAPI

from app.authentication.api.router import router as authentication_router
from app.files.router import router as files_router

app = FastAPI()

app.include_router(authentication_router)
app.include_router(files_router)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
