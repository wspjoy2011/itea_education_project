from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movies.models import Movie, Certification, Genre, MovieGenre, Director, MovieDirector, Star, MovieStar


class MovieReadSerializer(serializers.ModelSerializer):
    certification = serializers.CharField(source="certification.name")
    genres = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["uuid", "name", "year", "time", "imdb", "votes", "meta_score", "gross",
                  "description", "slug", "certification", "genres", "directors", "stars"]

    def get_genres(self, obj):
        return [movie_genre.genre.name for movie_genre in obj.movie_genres.all()]

    def get_directors(self, obj):
        return [movie_director.director.name for movie_director in obj.movie_directors.all()]

    def get_stars(self, obj):
        return [movie_star.star.name for movie_star in obj.movie_stars.all()]


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    certification_id = serializers.IntegerField()
    genre_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    director_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    star_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Movie
        fields = ["name", "year", "time", "imdb", "votes", "meta_score", "gross",
                  "description", "certification_id", "genre_ids", "director_ids", "star_ids"]

    def create(self, validated_data):
        certification_id = validated_data.pop('certification_id')
        genre_ids = validated_data.pop('genre_ids')
        director_ids = validated_data.pop('director_ids')
        star_ids = validated_data.pop('star_ids')

        with transaction.atomic():
            try:
                certification = Certification.objects.get(pk=certification_id)
            except Certification.DoesNotExist:
                raise ValidationError({
                    'certification_id': f'Certification with id {certification_id} not found'
                })

            movie = Movie.objects.create(certification=certification, **validated_data)

            for genre_id in genre_ids:
                try:
                    genre = Genre.objects.get(pk=genre_id)
                except Genre.DoesNotExist:
                    raise ValidationError({
                        'genre_ids': f'Genre with id {genre_id} not found'
                    })
                MovieGenre.objects.create(movie=movie, genre=genre)

            for director_id in director_ids:
                try:
                    director = Director.objects.get(pk=director_id)
                except Director.DoesNotExist:
                    raise ValidationError({
                        'director_ids': f'Director with id {director_id} not found'
                    })
                MovieDirector.objects.create(movie=movie, director=director)

            for star_id in star_ids:
                try:
                    star = Star.objects.get(pk=star_id)
                except Star.DoesNotExist:
                    raise ValidationError({
                        'stars_ids': f'Star with id {star_id} not found'
                    })
                MovieStar.objects.create(movie=movie, star=star)

        return movie














