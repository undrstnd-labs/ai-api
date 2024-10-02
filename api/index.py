from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.site import version, title, description
from api.routers import health, completion

app = FastAPI(
    title=title,
    version=version,
    description=description,
    docs_url="/api/py/docs", openapi_url="/api/py/openapi.json"
)

app.include_router(health.router)
app.include_router(completion.router)