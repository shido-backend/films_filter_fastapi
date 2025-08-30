from pydantic import BaseModel, Field
from typing import List, Optional

class Country(BaseModel):
    id: int
    country: str

class Genre(BaseModel):
    id: int
    genre: str

class FiltersResponse(BaseModel):
    genres: List[Genre]
    countries: List[Country]

class FilmCountry(BaseModel):
    country: str
    id: Optional[int] = None

class FilmGenre(BaseModel):
    genre: str
    id: Optional[int] = None 

class Film(BaseModel):
    kinopoiskId: int
    imdbId: Optional[str]
    nameRu: Optional[str]
    nameEn: Optional[str]
    nameOriginal: Optional[str]
    countries: List[FilmCountry]
    genres: List[FilmGenre]
    ratingKinopoisk: Optional[float]
    ratingImdb: Optional[float]
    year: int
    type: str
    posterUrl: str
    posterUrlPreview: str

class FilmsResponse(BaseModel):
    total: int
    totalPages: int
    items: List[Film]