from functools import wraps
from sanic.request import Request
from sanic.response import HTTPResponse, json


def check_active():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs) -> HTTPResponse:
            is_active = kwargs.get('user', {}).get('is_active', False)
            if not is_active:
                return json({"error": "Account not activated"}, 403)

            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator


def check_permission():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs) -> HTTPResponse:
            is_admin = kwargs.get('user', {}).get('admin', False)
            if is_admin:
                return json({"error": "Permission denied"}, 403)

            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
