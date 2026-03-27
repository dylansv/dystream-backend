# app/routers/watch.py

from fastapi import APIRouter
from services.vimeus_client import VimeusClient

router = APIRouter(prefix="/watch", tags=["watch"])

client = VimeusClient()


@router.get("")
async def watch(tmdb_id: int, type: str = "movie"):
    try:
        embed_url = await client.get_embed_url(tmdb_id, type)

        return {
            "embed_url": embed_url
        }

    except Exception as e:
        print("🔥 ERROR WATCH:", e)
        return {
            "embed_url": None,
            "error": "server_error"
        }