from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from movies.models import Movie
from api.serializers.movies import MovieReadSerializer, MovieCreateUpdateSerializer
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

    def post(self, request):
        create_serializer = MovieCreateUpdateSerializer(data=request.data)
        if create_serializer.is_valid():
            movie = create_serializer.save()
            read_serializer = MovieReadSerializer(movie)
            return Response({
                'result': read_serializer.data,
                'message': 'Movie added'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'errors': create_serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_authenticators(self):
        if self.request.method not in SAFE_METHODS:
            return [JWTAuthentication()]
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_object(self, uuid):
        return get_object_or_404(Movie, uuid=uuid)

    def get(self, request, uuid):
        movie = self.get_object(uuid)
        serializer = MovieReadSerializer(movie)
        return Response({
            'result': serializer.data
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        movie = self.get_object(uuid)
        serializer = MovieCreateUpdateSerializer(movie, data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({
                'result': MovieReadSerializer(movie).data,
                'message': 'Movie updated'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        movie = self.get_object(uuid)
        serializer = MovieCreateUpdateSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({
                'result': MovieReadSerializer(movie).data,
                'message': 'Movie updated'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        movie = self.get_object(uuid)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


















