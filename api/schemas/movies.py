from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse

from api.schemas.examples.errors import error_401_example, error_403_example, error_movie_400_required_fields_example, \
    error_movie_400_unique_constrain_example
from api.schemas.examples.movies import movie_example_response_json, movie_detail_example, movie_create_example
from api.serializers.movies import MovieReadSerializer, MovieCreateUpdateSerializer

movie_list_create_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve a list of movies. Allows filtering by several criteria.",
        parameters=[
            OpenApiParameter(
                name='year_min',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter movies released from this year (inclusive). Example: 1990',
                required=False
            ),
            OpenApiParameter(
                name='year_max',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter movies released until this year (inclusive). Example: 2020',
                required=False
            ),
            OpenApiParameter(
                name='certification_name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by certification name (case-insensitive). Multiple values can be provided,'
                            'separated by commas. Example: "pg-13,r"',
                required=False
            ),
            OpenApiParameter(
                name='genre_name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by genre name (case-insensitive). Multiple values can be provided,'
                            'separated by commas. Example: "action,drama"',
                required=False
            ),
            OpenApiParameter(
                name='top_movies',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter for top-rated movies (IMDB >= 7.0 AND MetaScore >= 80).'
                            'Example: true',
                required=False
            ),
            OpenApiParameter(
                name='era_filter',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by movie era. Possible values: "classic", "retro"',
                required=False
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Order the movies results by one or more fields. Multiple fields can be provided,"
                    "seperated by commas"
                    'Available fields: "name", "year", "time", "imdb", "votes", "meta_score", "gross"'
                    "Example: '-year,name'"
                ),
                required=False
            ),
        ],
        responses={
            200: MovieReadSerializer()
        },
        examples=[
            OpenApiExample(
                "Movie list example",
                value=movie_example_response_json
            )
        ]
    ),
    post=extend_schema(
        description="Create a new movie",
        request=MovieCreateUpdateSerializer,
        responses={
            201: MovieReadSerializer,
            400: OpenApiResponse(
                description='Bad request - Invalid data provided',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name='400 Not required fields provided',
                        value=error_movie_400_required_fields_example,
                        response_only=True
                    ),
                    OpenApiExample(
                        name='400 Unique constrains failed example',
                        value=error_movie_400_unique_constrain_example,
                        response_only=True
                    )
                ]
            ),
            401: OpenApiResponse(
                description='Unauthorized - No authentication credentials',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name='401 Unauthorized Example',
                        value=error_401_example,
                        response_only=True
                    )
                ]
            ),
            403: OpenApiResponse(
                description="Forbidden - You don't have permission to perform this action",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name='403 Forbidden Example',
                        value=error_403_example,
                        response_only=True
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                "Movie response example",
                value={
                    'result': movie_detail_example,
                    'message': 'Movie added'
                },
                response_only=True
            ),
            OpenApiExample(
                "Movie request example",
                value=movie_create_example,
                request_only=True
            ),
        ]
    )
)
