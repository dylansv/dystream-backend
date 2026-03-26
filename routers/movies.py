import httpx
from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.movie import MovieDetailResponse, MovieListResponse
from app.services.tmdb_client import TMDbClient

router = APIRouter(prefix="/movies", tags=["Movies"])

tmdb_client = TMDbClient()


@router.get("/popular", response_model=MovieListResponse)
async def get_popular_movies(
    page: int = Query(1, ge=1, description="Page number for popular movies"),
    language: str = Query("en-US", description="Response language, e.g. en-US, es-MX"),
):
    try:
        data = await tmdb_client.get_popular_movies(page=page, language=language)
        return data
    except httpx.HTTPStatusError as exc:
        detail = f"TMDb returned error {exc.response.status_code}: {exc.response.text}"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not connect to TMDb: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(exc)}") from exc


@router.get("/trending", response_model=MovieListResponse)
async def get_trending_movies(
    page: int = Query(1, ge=1, description="Page number for trending movies"),
    language: str = Query("en-US", description="Response language, e.g. en-US, es-MX"),
    time_window: str = Query("week", pattern="^(day|week)$", description="Trending window: day or week"),
):
    try:
        data = await tmdb_client.get_trending_movies(
            page=page,
            language=language,
            time_window=time_window,
        )
        return data
    except httpx.HTTPStatusError as exc:
        detail = f"TMDb returned error {exc.response.status_code}: {exc.response.text}"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not connect to TMDb: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(exc)}") from exc


@router.get("/search", response_model=MovieListResponse)
async def search_movies(
    query: str = Query(..., min_length=1, description="Movie search query"),
    page: int = Query(1, ge=1, description="Page number for search results"),
    language: str = Query("en-US", description="Response language, e.g. en-US, es-MX"),
    include_adult: bool = Query(False, description="Whether to include adult results"),
):
    try:
        data = await tmdb_client.search_movies(
            query=query,
            page=page,
            language=language,
            include_adult=include_adult,
        )
        return data
    except httpx.HTTPStatusError as exc:
        detail = f"TMDb returned error {exc.response.status_code}: {exc.response.text}"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not connect to TMDb: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(exc)}") from exc


@router.get("/{movie_id}", response_model=MovieDetailResponse)
async def get_movie_details(
    movie_id: int = Path(..., ge=1, description="TMDb movie ID"),
    language: str = Query("en-US", description="Response language, e.g. en-US, es-MX"),
):
    try:
        data = await tmdb_client.get_movie_details(movie_id=movie_id, language=language)
        return data
    except httpx.HTTPStatusError as exc:
        detail = f"TMDb returned error {exc.response.status_code}: {exc.response.text}"
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not connect to TMDb: {str(exc)}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(exc)}") from exc