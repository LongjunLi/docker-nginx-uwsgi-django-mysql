from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from backend.commons.customresponse import CustomResponse


class Page(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "size"
    page_query_param = "page"

    def get_paginated_response(self, data):
        return CustomResponse(data=data, code=200, msg="success", status=status.HTTP_200_OK, count=self.page.paginator.count,
                              total_page=self.page.paginator.num_pages, current_page=self.page.number,
                              next=self.get_next_link(), previous=self.get_previous_link())
