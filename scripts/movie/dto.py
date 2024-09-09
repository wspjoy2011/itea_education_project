from dataclasses import dataclass
from typing import Optional


@dataclass
class MovieDTO:
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    certification: str
    genres: set[str]
    directors: set[str]
    stars: set[str]
    description: str


@dataclass
class MoviesDTO:
    genres: set[str]
    directors: set[str]
    stars: set[str]
    certifications: set[str]
    movies: list[MovieDTO]
