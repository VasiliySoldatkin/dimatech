from sanic.request import Request
from sanic.response import HTTPResponse, json
from db.models import Users, Accounts
from sanic_jwt import inject_user, protected
from utils.auth import check_permission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, contains_eager
from sqlalchemy import select, update
from db.engine import engine


@check_permission()
@inject_user()
@protected()
async def get_users_with_accounts(request: Request, **kwargs) -> HTTPResponse:
    async_session = sessionmaker(engine, class_=AsyncSession)
    stmt = select(Users).join(Users.accounts).options(contains_eager(Users.accounts))
    result = []
    async with async_session() as session:
        data = (await session.execute(stmt)).unique().scalars()
        for user in data:
            user_data = {'id': user.id, 'login': user.login, 'is_active': user.is_active, 'accounts': []}
            for account in user.accounts:
                account = {'id': account.id, 'balance': account.balance}
                user_data['accounts'].append(account)
            result.append(user_data)
        await session.commit()

    return json(result)


@check_permission()
@inject_user()
@protected()
async def control_user(request: Request, user_id, activation, **kwargs) -> HTTPResponse:
    stmt = update(Users).filter(Users.id == user_id).values(is_active=activation == 'enable').returning(Users)
    async_session = sessionmaker(engine, AsyncSession)
    async with async_session() as session:
        result = (await session.execute(stmt)).first()
        if not result:
            return json({'error': "this user doesn't exists"}, status=400)
        await session.commit()
    return json(result)
