from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from movies.models import Movie
from api.serializers.movies import MovieReadSerializer
from api.pagination import CustomPagination
from api.orderings import MovieOrdering
from api.filters import MovieFilter


class MovieListAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter

    ordering_fields = ["name", "year", "time", "imdb", "votes", "meta_score", "gross"]

    def get(self, request):
        movies = Movie.objects.all()

        for backend in self.filter_backends:
            movies = backend().filter_queryset(request, movies, self)

        ordering = MovieOrdering.get_ordering_fields(request, self.ordering_fields)
        movies = movies.order_by(*ordering)

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(movies, request)

        serializer = MovieReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

