from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers.movies import router as movies_router, tmdb_client
from app.routers.watch import router as watch_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await tmdb_client.close()
    await vimeus_client.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")


@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


@app.get("/player.html")
async def serve_player():
    return FileResponse("frontend/player.html")


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/api", tags=["Health"])
async def api_root():
    return {
        "message": "DyStream API is running",
        "version": settings.app_version,
    }


app.include_router(movies_router)
app.include_router(watch_router)