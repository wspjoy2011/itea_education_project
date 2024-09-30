from datetime import datetime, timedelta

import django_filters
from django.utils import timezone

from blog.models import Post


class MultipleValuesUpperFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, values):
        if not values:
            return qs
        values = [value.strip().upper() for value in values]
        return super().filter(qs, values)


class MultipleValuesCapitalizeFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, qs, values):
        if not values:
            return qs
        values = [value.strip().capitalize() for value in values]
        return super().filter(qs, values)


class EraFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        era_years = self.get_years_for_era(value)
        if not era_years:
            return qs.none()
        return qs.filter(year__in=era_years)

    @staticmethod
    def get_movie_era(year: int) -> str:
        if 1900 <= year <= 1949:
            return 'classic'
        elif 1950 <= year <= 1979:
            return 'retro'
        elif 1980 <= year <= 1999:
            return 'old_school'
        elif 2000 <= year <= 2009:
            return 'early_modern'
        elif 2010 <= year <= datetime.today().year + 1:
            return 'early_modern'
        else:
            return 'unknown_era'

    @classmethod
    def get_years_for_era(cls, era: str) -> list[int]:
        return [year for year in range(1900, datetime.today().year + 1)
                if cls.get_movie_era(year) == era]


class MovieFilter(django_filters.FilterSet):
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    certification_name = MultipleValuesUpperFilter(field_name='certification__name')
    genre_name = MultipleValuesCapitalizeFilter(field_name='movie_genres__genre__name')
    top_movies = django_filters.BooleanFilter(method='filter_top_movies')
    era_filter = EraFilter()

    def filter_top_movies(self, queryset, name, value):
        if value:
            return queryset.filter(imdb__gte=7.0, meta_score__gte=80)
        return queryset


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username')
    publish = django_filters.NumberFilter(method='filter_by_days_ago')

    class Meta:
        model = Post
        fields = ['author', 'publish']

    def filter_by_days_ago(self, queryset, name, value):
        if value is not None:
            days_ago = int(value)
            start_date = timezone.now() - timedelta(days=days_ago)
            return queryset.filter(publish__gte=start_date)
        return queryset













