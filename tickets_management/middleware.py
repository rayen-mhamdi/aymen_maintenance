import re

class DeviceSpecificSessionCookieAgeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if re.search(r"Mobile|Tablet", user_agent):
            request.session.set_expiry(60 * 60 * 24 * 30) # 30 days
        else:
            request.session.set_expiry(60 * 5) # 5 minutes
        response = self.get_response(request)
        return response
