import ast
import csv
from abc import ABC, abstractmethod
from pathlib import Path

from tqdm import tqdm

from scripts.movie.dto import MoviesDTO, MovieDTO


class MovieParserInterface(ABC):
    @abstractmethod
    def read_csv_and_map_to_dto(self) -> MoviesDTO:
        pass


class MovieCSVParser(MovieParserInterface):
    def __init__(self, filename: str):
        self._filename = filename

    def _read_csv_file(self) -> list[list[str]]:
        rows = []
        with open(self._filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                rows.append(row[1:])
        return rows

    def _extract_unique_values(self, movies_rows: list[list[str]]):
        genres = set()
        directors = set()
        stars = set()
        certifications = set()

        for row in tqdm(movies_rows, desc='Converting data'):
            movie_genres = {row_genre.strip() for row_genre in ast.literal_eval(row[7])}
            genres.update(movie_genres)

            movie_directors = {movie_director.strip() for movie_director in ast.literal_eval(row[9])}
            directors.update(movie_directors)

            movie_stars = {movie_star.strip() for movie_star in ast.literal_eval(row[10])}
            stars.update(movie_stars)

            certification = row[8].strip()
            movie_certification = certification if certification else 'Not rated'
            certifications.add(movie_certification)

        return genres, directors, stars, certifications

    def _create_movie_dto(self, row: list[str]) -> MovieDTO:
        name = row[0].strip()
        year = int(row[1])
        time = int(row[2])
        imdb = float(row[3])
        votes = int(row[4])
        meta_score = float(row[5]) if row[5].strip() else None
        gross = float(row[6]) if row[6].strip() else None

        movie_genres = {row_genre.strip() for row_genre in ast.literal_eval(row[7])}
        movie_directors = {movie_director.strip() for movie_director in ast.literal_eval(row[9])}
        movie_stars = {movie_star.strip() for movie_star in ast.literal_eval(row[10])}
        certification = row[8].strip() if row[8].strip() else 'Not Rated'
        description = ' '.join([word.strip() for word in ast.literal_eval(row[11])])

        return MovieDTO(
            name=name,
            year=year,
            time=time,
            imdb=imdb,
            votes=votes,
            meta_score=meta_score,
            gross=gross,
            genres=movie_genres,
            directors=movie_directors,
            stars=movie_stars,
            certification=certification,
            description=description
        )

    def _map_rows_to_dto(self, movies_rows: list[list[str]]):
        genres, directors, stars, certifications = self._extract_unique_values(movies_rows)
        movies = [self._create_movie_dto(row) for row in movies_rows]
        return MoviesDTO(
            genres=genres,
            directors=directors,
            stars=stars,
            certifications=certifications,
            movies=movies
        )

    def read_csv_and_map_to_dto(self) -> MoviesDTO:
        movies_rows = self._read_csv_file()
        movies_dto = self._map_rows_to_dto(movies_rows)
        return movies_dto


if __name__ == '__main__':
    movies_csv_filename = str(Path(__file__).parent / 'data' / 'movies.csv')
    parser = MovieCSVParser(movies_csv_filename)
    movies = parser.read_csv_and_map_to_dto()

    for movie in movies.movies:
        print(movie.name, movie.year, movie.imdb, movie.certification)

