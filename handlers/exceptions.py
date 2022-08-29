from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from sanic.request import Request
from sanic.response import HTTPResponse, json

unknown_error = {'error': 'Unknown error', 'code': 400}


async def validation_error_handler(request: Request, exception: ValidationError) -> HTTPResponse:
    print(exception)
    return json(unknown_error if not exception.messages_dict else exception.messages_dict,
                status=400)


async def db_error_handler(request: Request, exception: IntegrityError):
    print(exception)
    return json(unknown_error)
