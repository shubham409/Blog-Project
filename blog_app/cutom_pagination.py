from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 7
    page_query_param= 'page'
    page_size_query_param= 'customsize'
    max_page_size = 6
    last_page_string = 'last'