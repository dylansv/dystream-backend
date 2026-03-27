# app/services/vimeus_client.py

from core.config import get_settings

settings = get_settings()


class VimeusClient:
    def __init__(self):
        self.base_url = settings.vimeus_base_url
        self.view_key = settings.vimeus_view_key

    async def get_embed_url(self, tmdb_id: int, content_type: str = "movie"):
        """
        Genera URL directa de embed sin depender del listing
        """

        if content_type == "movie":
            return f"{self.base_url}/e/movie?tmdb={tmdb_id}&view_key={self.view_key}"

        elif content_type == "tv":
            return f"{self.base_url}/e/serie?tmdb={tmdb_id}&view_key={self.view_key}"

        elif content_type == "anime":
            return f"{self.base_url}/e/anime?tmdb={tmdb_id}&view_key={self.view_key}"

        return None