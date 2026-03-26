from typing import List, Optional

from pydantic import BaseModel, Field


class MovieItem(BaseModel):
    id: int
    title: str
    original_title: str
    overview: str
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: float = 0.0
    vote_count: int = 0
    popularity: float = 0.0
    adult: bool = False
    original_language: str
    genre_ids: List[int] = Field(default_factory=list)


class MovieListResponse(BaseModel):
    page: int
    results: List[MovieItem]
    total_pages: int
    total_results: int


class GenreItem(BaseModel):
    id: int
    name: str


class ProductionCompany(BaseModel):
    id: int
    logo_path: Optional[str] = None
    name: str
    origin_country: str


class ProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class SpokenLanguage(BaseModel):
    english_name: str
    iso_639_1: str
    name: str


class MovieDetailResponse(BaseModel):
    id: int
    title: str
    original_title: str
    overview: str
    tagline: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    release_date: Optional[str] = None
    runtime: Optional[int] = None
    vote_average: float = 0.0
    vote_count: int = 0
    popularity: float = 0.0
    adult: bool = False
    original_language: str
    genres: List[GenreItem] = Field(default_factory=list)
    production_companies: List[ProductionCompany] = Field(default_factory=list)
    production_countries: List[ProductionCountry] = Field(default_factory=list)
    spoken_languages: List[SpokenLanguage] = Field(default_factory=list)
    status: Optional[str] = None
    homepage: Optional[str] = None
    imdb_id: Optional[str] = None
    budget: int = 0
    revenue: int = 0