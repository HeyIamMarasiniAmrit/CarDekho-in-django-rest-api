
from rest_framework.throttling import userRateThrottle

class ReviewDetailThrottle(userRateThrottle):
    scope = 'throttling_for_review_details'

class Reviewlistthrottle(userRateThrottle):
    scope = 'throttling_for_review_list'
