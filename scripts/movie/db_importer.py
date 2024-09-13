from pathlib import Path

from django.db import transaction
from tqdm import tqdm

# from scripts.movie import init_django_orm
from movies.models import (
    Certification,
    Director,
    Genre,
    Movie,
    MovieDirector,
    MovieGenre,
    MovieStar,
    Star
)
from scripts.movie.dto import MoviesDTO
from scripts.movie.csv_mapper import MovieCSVParser


class MovieDataImporter:
    def __init__(self, movies_dto: MoviesDTO):
        self._movies_dto = movies_dto

    def _get_or_create_certification(self, name: str) -> Certification:
        certification, _ = Certification.objects.get_or_create(name=name)
        return certification

    def _get_or_create_genre(self, name: str) -> Genre:
        genre, _ = Genre.objects.get_or_create(name=name)
        return genre

    def _get_or_create_director(self, name: str) -> Director:
        director, _ = Director.objects.get_or_create(name=name)
        return director

    def _get_or_create_star(self, name: str) -> Star:
        star, _ = Star.objects.get_or_create(name=name)
        return star

    @transaction.atomic
    def import_data(self) -> None:
        for movie_dto in tqdm(self._movies_dto.movies, desc='Populating db'):
            certification = self._get_or_create_certification(movie_dto.certification)

            movie = Movie(
                name=movie_dto.name,
                year=movie_dto.year,
                time=movie_dto.time,
                imdb=movie_dto.imdb,
                votes=movie_dto.votes,
                meta_score=movie_dto.meta_score,
                gross=movie_dto.gross,
                certification=certification,
                description=movie_dto.description
            )
            movie.save()

            for genre_name in movie_dto.genres:
                genre = self._get_or_create_genre(genre_name)
                MovieGenre.objects.create(movie=movie, genre=genre)

            for director_name in movie_dto.directors:
                director = self._get_or_create_director(director_name)
                MovieDirector.objects.create(movie=movie, director=director)

            for star_name in movie_dto.stars:
                star = self._get_or_create_star(star_name)
                MovieStar.objects.create(movie=movie, star=star)


if __name__ == '__main__':
    movies_csv_filename = str(Path(__file__).parent / 'data' / 'movies.csv')
    parser = MovieCSVParser(movies_csv_filename)
    movies_dto = parser.read_csv_and_map_to_dto()

    db_importer = MovieDataImporter(movies_dto)
    db_importer.import_data()





















