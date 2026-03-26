from typing import Any, Dict, Optional

import httpx

from app.core.config import get_settings


class TMDbClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.tmdb_api_key
        self.base_url = settings.tmdb_base_url.rstrip("/")
        self.default_language = "en-US"
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=20.0)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        query_params = params.copy() if params else {}
        query_params["api_key"] = self.api_key
        query_params.setdefault("language", self.default_language)

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        client = await self.get_client()

        response = await client.get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    async def get_popular_movies(
        self,
        page: int = 1,
        language: str = "en-US",
    ) -> Dict[str, Any]:
        return await self._get(
            endpoint="/movie/popular",
            params={
                "page": page,
                "language": language,
            },
        )

    async def get_trending_movies(
        self,
        page: int = 1,
        language: str = "en-US",
        time_window: str = "week",
    ) -> Dict[str, Any]:
        return await self._get(
            endpoint=f"/trending/movie/{time_window}",
            params={
                "page": page,
                "language": language,
            },
        )

    async def search_movies(
        self,
        query: str,
        page: int = 1,
        language: str = "en-US",
        include_adult: bool = False,
    ) -> Dict[str, Any]:
        return await self._get(
            endpoint="/search/movie",
            params={
                "query": query,
                "page": page,
                "language": language,
                "include_adult": str(include_adult).lower(),
            },
        )

    async def get_movie_details(
        self,
        movie_id: int,
        language: str = "en-US",
    ) -> Dict[str, Any]:
        return await self._get(
            endpoint=f"/movie/{movie_id}",
            params={
                "language": language,
            },
        )