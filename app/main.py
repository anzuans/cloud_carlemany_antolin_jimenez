from fastapi import FastAPI
<<<<<<< HEAD
from app.Authentication.router import router as authentication_router
from app.Files.router import router as files_router

app = FastAPI()

=======
from tortoise.contrib.fastapi import register_tortoise
from app.config import DATABASE_URL, models

from app.authentication.api.router import router as authentication_router
from app.files.api.router import router as files_router

app = FastAPI()

app.include_router(authentication_router)
app.include_router(files_router)

>>>>>>> activity-4

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

<<<<<<< HEAD
app.include_router(authentication_router)
app.include_router(files_router, prefix="/files")
=======
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": models},
    generate_schemas=True,
    add_exception_handlers=True,
)
>>>>>>> activity-4
