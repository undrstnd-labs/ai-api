from fastapi import FastAPI

from api.routers import completion, health, rag
from config.site import description, title, version

app = FastAPI(
    title=title,
    version=version,
    description=description,
    docs_url="/api/py/docs",
    openapi_url="/api/py/openapi.json",
)

app.include_router(health.router)
app.include_router(completion.router)
app.include_router(rag.router)
