from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import ValidationError

class ApiMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        response = self.get_response(request)

        # check auth and permission
        if not request.user.has_perm("rest_framework.permissions.IsAuthenticated"):
            raise ValidationError("Permission Denied")
        if not request.user.is_authenticated:
            raise ValidationError("User is not authenticated")

        # check is the headers has allows acces or not
        # if not request.headers.get("Allow-Access"):
        #     raise ValidationError("Allow-Access not found in headers")
        
        # check allowed IP address
        allowed_ips = ["127.0.0.1", "some ip range"]
        ip_address = request.META.get("REMOTE_ADDR")
        if ip_address not in allowed_ips:
            raise ValidationError("Access Denied. Your IP is not allowed")
        
        # check request limit: In this case, lets make request limit into 5 per minute
        # rate_limit = 5
        # key = f"ratelimit_{ip_address}"
        # count = cache.get(key)

        # if count is None:
        #     count = 1
        #     cache.set(key, count, 60)
        # else:
        #     count += 1
        #     cache.set(key, count, 60)
        
        # if count > rate_limit:
        #     raise ValidationError("Rate limit exceeded. Try again later")

        return response
