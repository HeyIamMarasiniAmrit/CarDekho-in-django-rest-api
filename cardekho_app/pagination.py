
from rest_framework.pagination import pageNumberpagination, LimitOffsetPagination, Cursorpagination

class Reviewlistpagination(pageNumberpagination):
    page_size = 2
    page_query_param = 'pa'
    page_size_query_param = 'size'
    max_page_size = 2
    last_page_strings = 'last'

class Reviewlistlimitoffpagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 3
    offset_query_param = 'start'
    limit_query_param = 'limitsss'

class Reviewlistcursorpag(Cursorpagination):
    page_size = 4
    ordering = 'created'
    page_size_query_param = 'size'
    max_page_size = 2
    last_page_strings = 'last
