from fastapi import Depends
import httpx
from typing import Optional
from src.models.kinopoisk import FiltersResponse, FilmsResponse
from src.config import settings
from src.exceptions.kinopoisk_exceptions import KinopoiskAPIError

class KinopoiskService:
    def __init__(self, client: httpx.AsyncClient = Depends(lambda: httpx.AsyncClient())):
        self.client = client
        self.headers = {
            "accept": "application/json",
            "X-API-KEY": settings.kinopoisk_api_key
        }

    async def get_filters(self) -> FiltersResponse:
        url = f"{settings.api_base_url}/filters"
        response = await self.client.get(url, headers=self.headers)
        if response.status_code != 200:
            raise KinopoiskAPIError(status_code=response.status_code, detail="Error fetching filters")
        data = response.json()

        excluded_genres = {"музыка", "концерт", "для взрослых"}
        filtered_genres = [
            genre for genre in data["genres"] 
            if genre["genre"] not in excluded_genres
        ]
        
        data["genres"] = filtered_genres
        return FiltersResponse(**data)

    async def get_films(
        self,
        country: Optional[int] = None,
        genre: Optional[int] = None,
        order: str = "RATING",
        type: str = "ALL",
        rating_from: float = 0,
        rating_to: float = 10,
        year_from: int = 1000,
        year_to: int = 3000,
        imdb_id: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1
    ) -> FilmsResponse:
        params = {
            "order": order,
            "type": type,
            "ratingFrom": rating_from,
            "ratingTo": rating_to,
            "yearFrom": year_from,
            "yearTo": year_to,
            "page": page
        }
        if country:
            params["countries"] = country
        if genre:
            params["genres"] = genre
        if imdb_id:
            params["imdbId"] = imdb_id
        if keyword:
            params["keyword"] = keyword

        response = await self.client.get(settings.api_base_url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise KinopoiskAPIError(status_code=response.status_code, detail="Error fetching films")
        data = response.json()

        excluded_genres = {"музыка", "концерт", "для взрослых"}
        filtered_items = [
            film for film in data["items"]
            if not any(genre["genre"] in excluded_genres for genre in film.get("genres", []))
        ]
        data["items"] = filtered_items

        return FilmsResponse(**data)