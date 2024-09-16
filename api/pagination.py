from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('previous', self.get_previous_link()),
            ('next', self.get_next_link()),
            ('pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('results', data),
        ]), status=status.HTTP_200_OK)
