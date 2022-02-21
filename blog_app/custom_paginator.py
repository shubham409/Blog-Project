from email.policy import default
from rest_framework.pagination import LimitOffsetPagination
class CustomPagination(LimitOffsetPagination):
    # when limit is not specifiec by client , client just provide offset
    default_limit = 3
    # key used for limit , default value is limit
    # limit_query_param = 'limit'
    # key used for offset , default value is offset
    # offset_query_param = 'offset'
    # max limit when client tries to use limit key with some value then
    max_limit = 3