from sanic.response import HTTPResponse, json
from sanic.request import Request
from serializers.schemas import RegisterSchema, UserSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import engine
from db.models import Users
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from sanic_jwt.exceptions import AuthenticationFailed
from sanic_jwt import BaseEndpoint


class Register(BaseEndpoint):
    async def post(self, request):
        body = request.json
        login, password = body.get('login'), body.get('password')
        if not (login or password):
            raise AuthenticationFailed("Missing username or password")
        async_session = sessionmaker(engine, AsyncSession)
        get_user = select(Users.id, Users.password).filter(Users.login == login)
        create_user = insert(Users).values(login=login, password=password)
        async with async_session() as session:
            data = (await session.execute(get_user)).first()
            if data is not None:
                raise AuthenticationFailed('There is already account with this login')
            await session.execute(create_user)

            await session.commit()

        return json({'activation_link': 'http://0.0.0.0:8000/register/verify/'})


class VerifyUser(BaseEndpoint):
    async def post(self, request):
        body = request.json
        login, password = body.get('login'), body.get('password')
        if not (login or password):
            raise AuthenticationFailed("Missing username or password")
        async_session = sessionmaker(engine, AsyncSession)
        get_user = select(Users.id, Users.password, Users.is_active).filter(Users.login == login)
        activate_user = update(Users).values(is_active=True).where(Users.login == login)
        async with async_session() as session:
            data = (await session.execute(get_user)).first()
            if data is None:
                raise AuthenticationFailed('No user with this login')

            db_id, db_password, db_is_active = data
            if db_password != password:
                raise AuthenticationFailed("Wrong password")

            if db_is_active:
                raise AuthenticationFailed('User is already verified')

            await session.execute(activate_user)

            await session.commit()

        return json({login: 'verified'})


async def retrieve_user(request, payload, *args, **kwargs):
    return payload


from sanic_jwt import Claim, Initialize


class AdminClaim(Claim):
    key = 'admin'

    @staticmethod
    def setup(payload, user):
        return user.get('admin', False)

    def verify(self, value):
        return True


async def jwt_auth(request: Request) -> dict:
    body = request.json
    login, password = body.get('login'), body.get('password')
    if not (login or password):
        raise AuthenticationFailed("Missing username or password")
    async_session = sessionmaker(engine, AsyncSession)
    get_user = select(Users.id, Users.password, Users.admin).filter(Users.login == login)
    async with async_session() as session:
        data = (await session.execute(get_user)).first()
        if not data:
            raise AuthenticationFailed("No user with this login")
        db_id, db_password, db_admin = data
        print(db_password)
        if db_password != password:
            raise AuthenticationFailed("Wrong password")
        await session.commit()

    return {'user_id': db_id, 'password': db_password, 'admin': db_admin}
