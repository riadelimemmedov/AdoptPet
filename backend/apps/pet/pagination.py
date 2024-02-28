from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# !PetPagination
class PetPagination(PageNumberPagination):
    page_size = 2  # Set the number of items per page
    cursor_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "pets": data,
            }
        )
