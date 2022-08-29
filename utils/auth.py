from functools import wraps
from sanic.request import Request
from sanic.response import HTTPResponse, json
from db.models import Users


def check_permission():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            if kwargs.get('user', {}).get('admin', False):
                return json({"error": "permission denied"}, 403)
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
