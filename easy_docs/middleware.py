from threading import local

_user_local = local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_local.user = request.user
        try:
            response = self.get_response(request)
        finally:
            if hasattr(_user_local, 'user'):
                del _user_local.user
        return response

    @classmethod
    def get_current_user(cls):
        return getattr(_user_local, 'user', None)