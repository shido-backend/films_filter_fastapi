from fastapi import APIRouter, Depends, Query
from typing import Optional
from src.models.kinopoisk import FiltersResponse, FilmsResponse
from src.services.kinopoisk_service import KinopoiskService

router = APIRouter(prefix="/api", tags=["films"])

@router.get("/filters", response_model=FiltersResponse)
async def fetch_filters(service: KinopoiskService = Depends()):
    return await service.get_filters()

@router.get("/films", response_model=FilmsResponse)
async def fetch_films(
    country: Optional[int] = Query(None, alias="countries"),
    genre: Optional[int] = Query(None, alias="genres"),
    order: str = Query("RATING"),
    type: str = Query("ALL"),
    rating_from: float = Query(0, alias="ratingFrom"),
    rating_to: float = Query(10, alias="ratingTo"),
    year_from: int = Query(1000, alias="yearFrom"),
    year_to: int = Query(3000, alias="yearTo"),
    imdb_id: Optional[str] = Query(None, alias="imdbId"),
    keyword: Optional[str] = Query(None),
    page: int = Query(1),
    service: KinopoiskService = Depends()
):
    return await service.get_films(
        country=country, genre=genre, order=order, type=type,
        rating_from=rating_from, rating_to=rating_to,
        year_from=year_from, year_to=year_to,
        imdb_id=imdb_id, keyword=keyword, page=page
    )