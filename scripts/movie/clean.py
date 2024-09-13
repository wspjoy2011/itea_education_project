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


class DataCleaner:
    def _delete_m2m(self) -> None:
        MovieDirector.objects.all().delete()
        MovieGenre.objects.all().delete()
        MovieStar.objects.all().delete()

    def _delete_stuff(self) -> None:
        Director.objects.all().delete()
        Genre.objects.all().delete()
        Star.objects.all().delete()

    def _delete_certification(self) -> None:
        Certification.objects.all().delete()

    def _delete_movies(self) -> None:
        Movie.objects.all().delete()

    def clean(self):
        self._delete_m2m()
        self._delete_stuff()
        self._delete_movies()
        self._delete_certification()


if __name__ == '__main__':
    DataCleaner().clean()
