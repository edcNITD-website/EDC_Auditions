from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


class GlobalRateLimitMiddleware:
    """
    Middleware to apply rate limits globally using django-ratelimit,
    with specific limits for certain routes (e.g., signup and login).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply rate limiting
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        # Route-specific rate limits
        if request.path == '/signup/':
            return self.apply_rate_limit(request, rate='10/h', key='ip')
        elif request.path == '/login/':
            return self.apply_rate_limit(request, rate='10/h', key='ip')

        # Global rate limit (fallback)
        return self.apply_rate_limit(request, rate='50/m', key='ip')

    def apply_rate_limit(self, request, rate, key):
        """
        Helper to apply a rate limit to the given request.
        """
        @ratelimit(key=key, rate=rate, block=True)
        def dummy_view(request):
            return None

        # Trigger rate limiting by calling the dummy view
        result = dummy_view(request)
        if hasattr(result, 'status_code') and result.status_code == 429:
            return JsonResponse(
                {"detail": "Rate limit exceeded. Try again later."},
                status=429
            )
        return None
