from scripts.movie import init_django_orm

from accounts.models import ActivateToken, PasswordResetToken, Profile, User
from blog.models import Category, Comment, CommentDislike, CommentLike, Follow, Post, PostDisLike, PostLike
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from movies.models import Certification, Director, Genre, Movie, MovieDirector, MovieGenre, MovieStar, Star
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery, Value, FloatField, IntegerField, CharField
from django.db.models.functions import Round

# filter year 2020 and imdb great then equal
movies = Movie.objects.filter(
    Q(year=2020) & Q(imdb__gte=8.0)
).order_by('-imdb', 'name')

# filter year not 2020 and imdb great then equal
movies = Movie.objects.filter(
    (~Q(year=2020) & Q(imdb__gte=8.0)) | Q(gross__gte=100000000)
).order_by('-imdb', 'name')

for movie in movies:
    print(f'{movie.name}, {movie.imdb}')

# select Horror from 2000 to 2020 and imdb greate then 7.0

horror_movies = Movie.objects.filter(
    movie_genres__genre__name='Horror',
    year__gte=2000,
    year__lte=2020,
    imdb__gt=7.0
).order_by('-imdb', 'name')

# select Horror or Action from 2000 to 2020 and imdb greate then 7.0

horror_action_movies = Movie.objects.filter(
    Q(movie_genres__genre__name='Horror') | Q(movie_genres__genre__name='Action'),
    year__gte=2000,
    year__lte=2020,
    imdb__gt=7.0
).order_by('-imdb', 'name')

# filter movies by actor name  Al Pacino

star_movies = Movie.objects.filter(
    movie_stars__star__name__icontains='Al Pacino'
).order_by('-imdb', 'name')

# top five genres by movies qty

popular_genres = Genre.objects.annotate(
    movie_count=Count('genre_movies')
).order_by('-movie_count')[:5]

for genre in popular_genres:
    print(f'{genre.name}, {genre.movie_count}')

# top five directors by average imdb rating

top_directors = Director.objects.annotate(
    avg_imdb=Round(Avg('director_movies__movie__imdb'), 1)
).order_by('-avg_imdb')[:5]

# top five directors by average imdb rating

top_directors_gt_five = Director.objects.filter(
    name__icontains='Tim'
).annotate(
    avg_imdb=Round(Avg('director_movies__movie__imdb'), 1),
    num_movies=Count('director_movies')
).filter(
    num_movies__gt=5
).order_by('-avg_imdb')[:5]

for director in top_directors_gt_five:
    print(f'{director.name}, {director.avg_imdb}')

# top ten actors by movie qty

top_actors = Star.objects.annotate(
    movie_count=Count('star_movies')
).order_by(
    '-movie_count'
)[:5]

# top five stars who play im movies by genre Horror

top_stars_in_horror_genre = Star.objects.filter(
    star_movies__movie__movie_genres__genre__name='Horror'
).annotate(
    movie_count=Count('star_movies')
).order_by(
    '-movie_count'
)[:5]

for star in top_stars_in_horror_genre:
    print(f'{star.name}, {star.movie_count}')

# top actor by genre

genres = Genre.objects.all()

for genre in genres:
    top_actor_by_genre = Star.objects.filter(
        star_movies__movie__movie_genres__genre=genre
    ).annotate(
        movie_count=Count('star_movies')
    ).order_by(
        '-movie_count'
    ).first()

    print(genre.name, top_actor_by_genre.name, top_actor_by_genre.movie_count)

# find movies which contain search word

word = 'world'
find_movies = Movie.objects.filter(
    Q(name__icontains=word) | Q(description__icontains=word)
)

# find movies which contain search word by range

find_movies = Movie.objects.annotate(
    relevance=Case(
        When(
            name__icontains=word,
            description__icontains=word,
            then=Value(0.3)
        ),
        When(
            name__icontains=word,
            then=Value(0.2)
        ),
        When(
            description__icontains=word,
            then=Value(0.1)
        ),
        default=Value(0.0),
        output_field=FloatField()
    )
).filter(
    relevance__gt=0.0
).order_by(
    '-relevance'
)[:10]

for movie in find_movies:
    print(movie.name, movie.description)

# count qty result by previous query

genre_movie_counts = Genre.objects.filter(
    Q(genre_movies__movie__name__icontains=word) | Q(genre_movies__movie__description__icontains=word)
).annotate(
    num_movies=Count('genre_movies')
).order_by(
    '-num_movies'
)

for genre in genre_movie_counts:
    print(genre.name, genre.num_movies)

genres = Genre.objects.annotate(
    top_star_id=Subquery(
        MovieStar.objects.filter(
            movie__movie_genres__genre=OuterRef('pk')
        ).values(
            'star'
        ).annotate(
            total=Count('movie')
        ).order_by(
            '-total'
        ).values('star')[:1],
        output_field=IntegerField()
    )
).annotate(
    top_star_name=Subquery(
        Star.objects.filter(
            id=OuterRef('top_star_id')
        ).values('name')[:1],
        output_field=CharField()
    ),
    num_movies=Subquery(
        MovieStar.objects.filter(
            star=OuterRef('top_star_id'),
            movie__movie_genres__genre=OuterRef('pk')
        ).values('star').annotate(
            total=Count('movie')
        ).values('total')[:1],
        output_field=IntegerField()
    )
).values(
    'name', 'top_star_name', 'num_movies'
).order_by(
    'name'
)

for genre in genres:
    print(genre)

