from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.config import get_settings
from routers.movies import router as movies_router, tmdb_client
from routers.watch import router as watch_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await tmdb_client.close()
    # ⚠️ Quitamos vimeus_client porque no está definido
    # await vimeus_client.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# 🔥 CORS abierto para que frontend (Vercel / local / app) funcione
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 🌐 Frontend básico (opcional)
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


@app.get("/player.html")
async def serve_player():
    return FileResponse("frontend/player.html")


# 🧪 Health check
@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


# 🧠 API root
@app.get("/api", tags=["Health"])
async def api_root():
    return {
        "message": "DyStream API is running",
        "version": settings.app_version,
    }


# 🎬 Rutas principales
app.include_router(movies_router)
app.include_router(watch_router)