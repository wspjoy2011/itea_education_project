import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField


class StaffMovie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(
        max_length=100, populate_from=['name']
    )

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(StaffMovie):
    pass


class Star(StaffMovie):
    pass


class Director(StaffMovie):
    pass


class Certification(StaffMovie):
    pass


class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    time = models.IntegerField()
    imdb = models.FloatField()
    votes = models.IntegerField()
    meta_score = models.FloatField(null=True, blank=True)
    gross = models.FloatField(null=True, blank=True)
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT, related_name='movies')
    description = models.TextField()
    slug = AutoSlugField(max_length=100, populate_from=['name'])

    class Meta:
        ordering = ('name', 'year')

    def __str__(self):
        return f'{self.name} - {self.year}'


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_movies')

    class Meta:
        unique_together = ('movie', 'genre')

    def __str__(self):
        return f'{self.movie} - {self.genre}'


class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_directors')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')

    class Meta:
        unique_together = ('movie', 'director')

    def __str__(self):
        return f'{self.movie} - {self.director}'


class MovieStar(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_stars')
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name='star_movies')

    class Meta:
        unique_together = ('movie', 'star')

    def __str__(self):
        return f'{self.movie} - {self.star}'
