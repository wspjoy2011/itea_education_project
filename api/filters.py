import django_filters


class MultipleValuesUpperFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, values):
        if not values:
            return qs
        values = [value.upper() for value in values]
        return super().filter(qs, values)


class MultipleValuesCapitalizeFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, values):
        if not values:
            return qs
        values = [value.capitalize() for value in values]
        return super().filter(qs, values)


class MovieFilter(django_filters.FilterSet):
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    certification_name = MultipleValuesUpperFilter(field_name='certification__name')
    genre_name = MultipleValuesCapitalizeFilter(field_name='movie_genres__genre__name')
    top_movies = django_filters.BooleanFilter(method='filter_top_movies')

    def filter_top_movies(self, queryset, name, value):
        if value:
            return queryset.filter(imdb__gte=7.0, meta_score__gte=80)
        return queryset

















