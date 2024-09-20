from rest_framework import serializers

from movies.models import Movie


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
















