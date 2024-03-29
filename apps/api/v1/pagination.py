from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 10
    page_size_query_param = 'limit'
