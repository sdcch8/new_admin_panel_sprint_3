from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 50

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': self.get_previous_page_number(),
            'next': self.get_next_page_number(),
            'results': data
        })
